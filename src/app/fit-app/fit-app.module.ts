import { NgModule } from "@angular/core";
import { CommonModule } from "@angular/common";

import { DashboardComponent } from "./dashboard/dashboard.component";
import { UserProfileComponent } from "./user-profile/user-profile.component";

import { SharedModule } from "app/shared/shared.module";
import { FitAppRoutingModule } from "./fit-app-routing.module";
import { FitAppComponent } from "./fit-app.component";
import { ComponentsModule } from "./components/components.module";
import { TrackComponent } from "./track/track.component";
import { HistoryComponent } from "./history/history.component";
import { TestDataComponent } from "./test-data/test-data.component";

@NgModule({
  imports: [CommonModule, ComponentsModule, SharedModule, FitAppRoutingModule],
  declarations: [
    DashboardComponent,
    UserProfileComponent,
    FitAppComponent,
    TrackComponent,
    HistoryComponent,
    TestDataComponent,
  ],
  bootstrap: [FitAppComponent],
})
export class FitAppModule {}
