import { BrowserAnimationsModule } from "@angular/platform-browser/animations";
import { NgModule } from "@angular/core";
import { AppRoutingModule } from "./app.routing";
import { AppComponent } from "./app.component";
import { HomeComponent } from "./home/home.component";
import { SharedModule } from "./shared/shared.module";
import { FitAppModule } from "./fit-app/fit-app.module";
import { HttpModule } from "@angular/http";
import { HttpClientModule, HTTP_INTERCEPTORS } from "@angular/common/http";
import { AuthInterceptor } from "./auth/auth.interceptor";
import { DatePipe } from "@angular/common";

@NgModule({
  imports: [
    BrowserAnimationsModule,
    AppRoutingModule,
    SharedModule,
    FitAppModule,
    HttpClientModule,
    HttpModule,
  ],
  declarations: [AppComponent, HomeComponent],
  providers: [
    { provide: HTTP_INTERCEPTORS, useClass: AuthInterceptor, multi: true },
    DatePipe,
  ],
  bootstrap: [AppComponent],
})
export class AppModule {}
