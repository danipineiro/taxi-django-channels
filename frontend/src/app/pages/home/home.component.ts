import {Component, OnInit} from '@angular/core';
import {MatAnchor, MatButton} from "@angular/material/button";
import {TripService} from "../../services/trip.service";
import {CurrentUserDTO} from "../../models/current-user-dto";
import {DRIVER, PASSENGER} from "../../shared/constants/user-types";
import {UserService} from "../../services/user.service";
import {NgForOf, NgIf} from "@angular/common";
import {Trip, tripStatus} from "../../models/trip-dto";
import {TripComponent} from "../trip/trip.component";

@Component({
  selector: 'app-home',
  standalone: true,
  imports: [
    MatAnchor,
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
    private userService: UserService
  ) {
  }

  ngOnInit() {
    this.userService.getCurrentUser().subscribe((user) => {
      this.currentUser = user;
      this.loadTrips();
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

  refreshTrips($event: boolean) {
    if ($event) {
      this.loadTrips();
    }
  }

  /**
   * This method is used to disable the creation of a new trip.
   * It sets the `disableCreateTrip` property to `true` if there exists a trip that is either requested, started, or accepted.
   * This is to ensure that a user cannot create a new trip if there is a trip that is already in one of these states.
   */
  disableCreteTrip() {
    this.disableCreateTrip = this.trips.some((trip) => [tripStatus.Requested, tripStatus.Started, tripStatus.Accepted].includes(trip.status));
  }
}
