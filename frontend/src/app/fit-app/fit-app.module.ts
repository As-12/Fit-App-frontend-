import { NgModule } from "@angular/core";
import { CommonModule } from "@angular/common";

import { DashboardComponent } from "./dashboard/dashboard.component";
import { UserProfileComponent } from "./user-profile/user-profile.component";
import { TableListComponent } from "./table-list/table-list.component";

import { SharedModule } from "app/shared/shared.module";
import { FitAppRoutingModule } from "./fit-app-routing.module";
import { FitAppComponent } from "./fit-app.component";
import { ComponentsModule } from "./components/components.module";
import { TypographyComponent } from "./typography/typography.component";

@NgModule({
  imports: [CommonModule, ComponentsModule, SharedModule, FitAppRoutingModule],
  declarations: [
    DashboardComponent,
    UserProfileComponent,
    TableListComponent,
    FitAppComponent,
    TypographyComponent,
  ],
  bootstrap: [FitAppComponent],
})
export class FitAppModule {}
