import { BrowserAnimationsModule } from "@angular/platform-browser/animations";
import { NgModule } from "@angular/core";
import { AppRoutingModule } from "./app.routing";
import { AppComponent } from "./app.component";
import { AdminLayoutComponent } from "./layouts/admin-layout/admin-layout.component";
import { HomeComponent } from "./home/home.component";
import { SharedModule } from "./shared/shared.module";

@NgModule({
  imports: [BrowserAnimationsModule, AppRoutingModule, SharedModule],
  declarations: [AppComponent, AdminLayoutComponent, HomeComponent],
  providers: [],
  bootstrap: [AppComponent],
})
export class AppModule {}
