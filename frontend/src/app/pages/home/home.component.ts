import {Component, OnInit} from '@angular/core';
import {MatButton} from "@angular/material/button";
import {TripService} from "../../services/trip.service";
import {CurrentUserDTO} from "../../models/current-user-dto";
import {DRIVER, PASSENGER} from "../../shared/constants/user-types";
import {UserService} from "../../services/user.service";
import {NgForOf, NgIf} from "@angular/common";
import {Trip, tripStatus} from "../../models/trip-dto";
import {TripComponent} from "../trip/trip.component";
import {WebsocketService} from "../../services/websocket.service";
import {createWebpackLoggingCallback} from "@angular-devkit/build-angular/src/tools/webpack/utils/stats";

@Component({
  selector: 'app-home',
  standalone: true,
  imports: [
    MatButton,
    NgIf,
    TripComponent,
    NgForOf
  ],
  templateUrl: './home.component.html',
  styleUrl: './home.component.scss'
})
export class HomeComponent implements OnInit {
  protected readonly PASSENGER = PASSENGER;

  public trips: Trip[] = [];
  currentUser!: CurrentUserDTO;
  disableCreateTrip = true;

  constructor(
    private readonly tripService: TripService,
    private userService: UserService,
    private websocketService: WebsocketService
  ) {
  }

  ngOnInit() {
    this.userService.getCurrentUser().subscribe((user) => {
      this.currentUser = user;
      this.loadTrips();
    });

    this.connectWebSocket();

  }

  loadTrips() {
    if (this.currentUser.type === DRIVER) {
      this.tripService.getDriverTrips().subscribe((trips: Trip[]) => {
        this.trips = trips;
      });
    } else if (this.currentUser.type === PASSENGER) {
      this.tripService.getPassengerTrips().subscribe((trips: Trip[]) => {
        this.trips = trips;
        this.disableCreteTrip();
      });
    }
  }

  /**
   * Establishes a WebSocket connection and subscribes to incoming messages.
   *
   * This method connects to the WebSocket server at the specified URL and sets up a subscription
   * to handle incoming messages. The messages are processed by the `handleWebSocketMessage` method.
   */
  private connectWebSocket() {
    this.websocketService.connect('ws://localhost:8001/ws/trip/');

    this.websocketService.getMessages().subscribe(
      message => this.handleWebSocketMessage(message)
    );
  }

  /**
   * Handles incoming WebSocket messages and updates the trip list accordingly.
   *
   * This method processes different types of WebSocket messages:
   * - 'trip_update': Updates the trip list with the provided trip data.
   * - 'trip_deleted': Removes the trip with the specified ID from the trip list.
   * - Default: Logs a warning for unknown message types.
   *
   * After processing the message, it calls `disableCreteTrip` to update the state of trip creation.
   *
   * @param message - The WebSocket message to handle. It should contain a `type` and `content`.
   */
  private handleWebSocketMessage(message: any) {
    switch (message?.type) {
      case 'trip_update':
        this.handleTripUpdate(message.content);
        break;

      case 'trip_deleted':
        this.trips = this.trips.filter(trip => trip.id !== message.content.id);
        break;

      default:
        console.warn('Mensaje WebSocket desconocido:', message);
        break;
    }

    this.disableCreteTrip();
  }

  createTrip() {
    this.tripService.createTrip().subscribe((trip) => {
      this.loadTrips();
    });
  }

  /**
   * This method is used to disable the creation of a new trip.
   * It sets the `disableCreateTrip` property to `true` if there exists a trip that is either requested, started, or accepted.
   * This is to ensure that a user cannot create a new trip if there is a trip that is already in one of these states.
   */
  disableCreteTrip() {
    this.disableCreateTrip = this.trips.some((trip) => [tripStatus.Requested, tripStatus.Started, tripStatus.Accepted].includes(trip.status));
  }

  /**
   * Updates the list of trips with the provided trip data.
   * If a trip with the same ID exists in the list, it is replaced with the updated data.
   * If no trip with the same ID exists, the new trip is added to the list.
   *
   * @param updatedTrip - The trip object containing updated or new data.
   */
  handleTripUpdate(updatedTrip: Trip): void {
    const tripIndex = this.trips.findIndex(trip => trip.id === updatedTrip.id);

    if (tripIndex > -1) {
      this.trips = [
        ...this.trips.slice(0, tripIndex),
        updatedTrip,
        ...this.trips.slice(tripIndex + 1)
      ];
    } else {
      this.trips = [updatedTrip, ...this.trips];
    }
  }
}
