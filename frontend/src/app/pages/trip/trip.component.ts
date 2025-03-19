import {Component, Input, OnInit} from '@angular/core';
import {Trip, tripStatus} from "../../models/trip-dto";
import {MatButton} from '@angular/material/button';
import {MatCardModule} from '@angular/material/card';
import {DatePipe, NgIf} from "@angular/common";
import {TripService} from "../../services/trip.service";
import {CurrentUserDTO} from "../../models/current-user-dto";
import {DRIVER, PASSENGER} from "../../shared/constants/user-types";


@Component({
  selector: 'app-trip',
  standalone: true,
  imports: [
    MatCardModule,
    DatePipe,
    MatButton,
    NgIf,
  ],
  templateUrl: './trip.component.html',
  styleUrl: './trip.component.scss'
})
export class TripComponent implements OnInit {
  @Input() trip!: Trip;
  @Input() currentUser!: CurrentUserDTO;

  protected readonly PASSENGER = PASSENGER;
  protected readonly DRIVER = DRIVER;
  protected readonly tripStatus = tripStatus;

  constructor(
    private tripService: TripService
  ) {
  }

  ngOnInit() {
  }

  deleteTrip() {
    this.tripService.deleteTrip(this.trip.id).subscribe(() => {
    });
  }

  acceptTrip() {
    this.tripService.acceptTrip(this.trip.id).subscribe(() => {
    });
  }

  startTrip() {
    this.tripService.startTrip(this.trip.id).subscribe(() => {
    });
  }

  completeTrip() {
    this.tripService.completeTrip(this.trip.id).subscribe(() => {
    });
  }

}
