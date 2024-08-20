import {Injectable} from '@angular/core';
import {HttpClient} from "@angular/common/http";

@Injectable({
  providedIn: 'root'
})
export class UserService {
  private apiUrl = 'http://localhost:8000/api/v1';

  constructor(private http: HttpClient) {
  }

  getCurrentUser() {
    return this.http.get(`${this.apiUrl}/profile/`,);
  }
}
