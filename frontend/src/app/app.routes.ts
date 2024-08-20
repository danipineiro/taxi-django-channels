import { Routes } from '@angular/router';
import {LoginComponent} from "./pages/login/login.component";
import {HomeComponent} from "./pages/home/home.component";
import {isLoggedGuard} from "./guards/is-logged.guard";

export const routes: Routes = [
  {
    path: '',
    component: HomeComponent,
    canActivate: [isLoggedGuard],
    title: 'Home page'
  },

  {
    path: 'login',
    component: LoginComponent,
    title: 'Login page'
  },
];
