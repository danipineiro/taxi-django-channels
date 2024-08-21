import {Injectable} from '@angular/core';
import {HttpClient} from "@angular/common/http";
import {Observable} from "rxjs";
import {environment} from "../../environments/environment";


@Injectable({
  providedIn: 'root'
})
export class UserService {
  private apiUrl = `${environment.host}api/v1/`;

  constructor(private http: HttpClient) {
  }

  getCurrentUser(): Observable<any> {
    return this.http.get(`${this.apiUrl}profile/`,);
  }
}
