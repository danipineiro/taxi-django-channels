import {Component, OnInit} from '@angular/core';
import {MatAnchor, MatButton} from "@angular/material/button";
import {TripService} from "../../services/trip.service";
import {CurrentUserDTO} from "../../models/current-user-dto";
import {DRIVER, PASSENGER} from "../../shared/constants/user-types";
import {UserService} from "../../services/user.service";
import {NgIf} from "@angular/common";

@Component({
  selector: 'app-home',
  standalone: true,
  imports: [
    MatAnchor,
    MatButton,
    NgIf
  ],
  templateUrl: './home.component.html',
  styleUrl: './home.component.scss'
})
export class HomeComponent implements OnInit {
  protected readonly PASSENGER = PASSENGER;

  public trips: any[] = [];
  currentUser!: CurrentUserDTO;

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
      this.tripService.getDriverTrips().subscribe((trips) => {
        this.trips = trips;
      });
    } else if (this.currentUser.type === PASSENGER) {
      this.tripService.getPassengerTrips().subscribe((trips) => {
        this.trips = trips;
      });
    }
  }

  createTrip() {
    this.tripService.createTrip().subscribe((trip) => {
      console.log(trip);
    });
  }

}
