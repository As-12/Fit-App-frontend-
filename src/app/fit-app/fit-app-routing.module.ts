import { NgModule } from "@angular/core";
import { Routes, RouterModule } from "@angular/router";
import { DashboardComponent } from "./dashboard/dashboard.component";
import { UserProfileComponent } from "./user-profile/user-profile.component";
import { TrackComponent } from "./track/track.component";
import { HistoryComponent } from "./history/history.component";
import { TestDataComponent } from "./test-data/test-data.component";

const routes: Routes = [
  { path: "", redirectTo: "dashboard", pathMatch: "full" },
  { path: "dashboard", component: DashboardComponent },
  { path: "user-profile", component: UserProfileComponent },
  { path: "track", component: TrackComponent },
  { path: "history", component: HistoryComponent },
  { path: "test", component: TestDataComponent },
];

@NgModule({
  imports: [RouterModule.forChild(routes)],
  exports: [RouterModule],
})
export class FitAppRoutingModule {}
