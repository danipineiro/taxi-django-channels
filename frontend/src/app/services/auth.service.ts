import {Injectable} from '@angular/core';
import {HttpClient} from '@angular/common/http';
import {Observable} from 'rxjs';
import {LoginDTO} from "../models/login-dto";
import {RegisterDTO} from "../models/register-dto";

@Injectable({
  providedIn: 'root'
})
export class AuthService {

  private apiUrl = 'http://localhost:8000/api/v1';

  constructor(private http: HttpClient) {
  }

  login(loginDTO: LoginDTO): Observable<any> {
    return this.http.post(`${this.apiUrl}/signin`, loginDTO);
  }

  register(registerDTO: RegisterDTO): Observable<any> {
    return this.http.post(`${this.apiUrl}/signup/`, registerDTO);
  }

  logout() {
    localStorage.removeItem('token');
    return this.http.post(`${this.apiUrl}/logout`, {});
  }

  refreshToken() {
    return this.http.post(`${this.apiUrl}/token/refresh/`, {});
  }

}
