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

    this.websocketService.connect('ws://localhost:8001/ws/trip/');

    this.websocketService.getMessages().subscribe((message) => {
      const trip: Trip = message['content']
      this.handleTripUpdate(trip);
    });

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
