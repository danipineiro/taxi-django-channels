import {EventEmitter, Injectable} from '@angular/core';
import {HttpClient} from '@angular/common/http';
import {Observable} from 'rxjs';
import {LoginDTO} from "../models/login-dto";
import {RegisterDTO} from "../models/register-dto";

@Injectable({
  providedIn: 'root'
})
export class AuthService {

  private apiUrl = 'http://localhost:8000/api/v1';

  loggedChanged$ = new EventEmitter<boolean>();

  constructor(private http: HttpClient) {
  }

  login(loginDTO: LoginDTO): Observable<any> {
    return this.http.post(`${this.apiUrl}/signin/`, loginDTO);
  }

  register(registerDTO: RegisterDTO): Observable<any> {
    return this.http.post(`${this.apiUrl}/signup/`, registerDTO);
  }

  logout() {
    localStorage.removeItem('access');
    localStorage.removeItem('refresh');
    localStorage.removeItem('currentUser');
    this.loggedChanged$.emit(false);
  }

  refreshToken() {
    const body = {
      refresh: localStorage.getItem('refresh')
    }
    this.http.post(`${this.apiUrl}/token/refresh/`, body).subscribe({
      next: (response: any) => {
        this.setAccessToken(response.access);
      },
      error: (error) => {
        console.error(error);
      }
    });
  }

  getAccessToken() {
    return localStorage.getItem('access');
  }

  setAccessToken(token: string) {
    localStorage.setItem('access', token);
    this.loggedChanged$.emit(true);
  }

  setRefreshToken(token: string) {
    localStorage.setItem('refresh', token);
  }

  isLogged() {
    return !!localStorage.getItem('access');
  }
}
