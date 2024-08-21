import {Component, OnInit} from '@angular/core';
import {MatAnchor, MatButton} from "@angular/material/button";
import {TripService} from "../../services/trip.service";
import {CurrentUserDTO} from "../../models/current-user-dto";
import {DRIVER, PASSENGER} from "../../shared/constants/user-types";
import {UserService} from "../../services/user.service";

@Component({
  selector: 'app-home',
  standalone: true,
  imports: [
    MatAnchor,
    MatButton
  ],
  templateUrl: './home.component.html',
  styleUrl: './home.component.scss'
})
export class HomeComponent implements OnInit {
  public trips: any[] = [];

  constructor(
    private readonly tripService: TripService,
    private userService: UserService
  ) {
  }

    ngOnInit() {
    this.userService.getCurrentUser().subscribe((user: CurrentUserDTO) => {
      if (user.type === DRIVER) {
        this.getDriverTrips();
      } else if (user.type === PASSENGER) {
        this.getPassengerTrips();
      }
    });
  }

  createTrip() {
    this.tripService.createTrip().subscribe((trip) => {
      console.log(trip);
    });
  }

    getPassengerTrips() {
    this.tripService.getPassengerTrips().subscribe((trips) => {
      this.trips = trips;
      console.log(trips);
    });
  }

  getDriverTrips() {
    this.tripService.getDriverTrips().subscribe((trips) => {
      this.trips = trips;
    });
  }
}
