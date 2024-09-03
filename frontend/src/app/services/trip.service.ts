import { Injectable } from '@angular/core';
import {environment} from "../../environments/environment";
import {HttpClient} from "@angular/common/http";
import {Observable} from "rxjs";

@Injectable({
  providedIn: 'root'
})
export class TripService {

  private apiUrl = `${environment.host}api/v1/trip/`;

  constructor(private http: HttpClient) {
  }

  getPassengerTrips(): Observable<any> {
    return this.http.get(`${this.apiUrl}passenger/`);
  }

  createTrip(): Observable<any> {
    return this.http.post(`${this.apiUrl}passenger/`, {});
  }

  getDriverTrips(): Observable<any> {
    return this.http.get(`${this.apiUrl}driver/`);
  }

  deleteTrip(id: number): Observable<any> {
    return this.http.delete(`${this.apiUrl}passenger/${id}/`);
  }

  acceptTrip(id: number): Observable<any> {
    return this.http.post(`${this.apiUrl}driver/${id}/accept/`, {});
  }

  startTrip(id: number): Observable<any> {
    return this.http.post(`${this.apiUrl}driver/${id}/start/`, {});
  }

  completeTrip(id: number): Observable<any> {
    return this.http.post(`${this.apiUrl}driver/${id}/complete/`, {});
  }

}
