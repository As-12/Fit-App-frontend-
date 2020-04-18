import { Component, OnInit } from "@angular/core";
import { AuthService } from "app/auth/auth.service";

@Component({
  selector: "app-user-profile",
  templateUrl: "./user-profile.component.html",
  styleUrls: ["./user-profile.component.css"],
})
export class UserProfileComponent implements OnInit {
  constructor(private auth: AuthService) {}

  ngOnInit() {}
}
