import { Component } from '@angular/core';
import {MatAnchor, MatButton} from "@angular/material/button";
import {TripService} from "../../services/trip.service";

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
export class HomeComponent {

  constructor(
    private readonly tripService: TripService,
  ) {
  }

  createTrip() {
    this.tripService.createTrip().subscribe((trip) => {
      console.log(trip);
    });
  }
}
