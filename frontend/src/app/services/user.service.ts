import {Injectable} from '@angular/core';
import {HttpClient} from "@angular/common/http";
import {Observable, of, tap} from "rxjs";
import {environment} from "../../environments/environment";


@Injectable({
  providedIn: 'root'
})
export class UserService {
  private apiUrl = `${environment.host}api/v1/`;

  constructor(private http: HttpClient) {
  }

getCurrentUser(): Observable<any> {
    const currentUser = localStorage.getItem('currentUser');
    if (currentUser) {
      return of(JSON.parse(currentUser));
    } else {
      return this.http.get(`${this.apiUrl}profile/`).pipe(
        tap(user => localStorage.setItem('currentUser', JSON.stringify(user)))
      );
    }
  }
}
