import { NgModule } from "@angular/core";
import { CommonModule } from "@angular/common";
import { BrowserModule } from "@angular/platform-browser";
import { Routes, RouterModule } from "@angular/router";

import { HomeComponent } from "./home/home.component";

const routes: Routes = [
  {
    path: "",
    component: HomeComponent,
  },
  {
    path: "fit-app",
    redirectTo: "fit-app/dashboard",
    pathMatch: "full",
  },
  {
    // Lazy loading the feature
    path: "fit-app",
    loadChildren: () =>
      import("./fit-app/fit-app.module").then((m) => m.FitAppModule),
  },
];

@NgModule({
  imports: [CommonModule, BrowserModule, RouterModule.forRoot(routes)],
  exports: [],
})
export class AppRoutingModule {}
