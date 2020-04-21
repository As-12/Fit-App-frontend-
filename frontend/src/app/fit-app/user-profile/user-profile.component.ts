import { Component, OnInit, ElementRef } from "@angular/core";
import { AuthService } from "app/auth/auth.service";
import { UserService } from "../services/user.service";
import { NotificationService } from "../services/notification.service";
import { User } from "../model/user.model";
import { NgForm } from "@angular/forms";

@Component({
  selector: "app-user-profile",
  templateUrl: "./user-profile.component.html",
  styleUrls: ["./user-profile.component.css"],
})
export class UserProfileComponent implements OnInit {
  constructor(
    public auth: AuthService,
    public userService: UserService,
    public notification: NotificationService
  ) {}

  private submitButton: ElementRef;

  private isSubmitDisabled: boolean = false;

  protected user: User;

  ngOnInit() {
    this.userService.user$.subscribe((user) => {
      this.user = user;
    });
  }

  validateUser() {
    //Bugfix: Ngmodel binding seems to cast the number to string
    this.user.target_weight = +this.user.target_weight;
    this.user.height = +this.user.target_weight;
  }

  updateUser(form: NgForm): void {
    this.isSubmitDisabled = true;
    console.log("Submitting");
    this.validateUser();
    this.userService.updateUser(this.user).subscribe(
      (res) => {
        this.notification.showNotification(
          "User profile has been updated",
          "success"
        );
        this.isSubmitDisabled = false;
      },
      (err) => {
        if (err.status === 400 || err.status === 422) {
          this.notification.showNotification(
            `Unable to update user profile due to invalid data`,
            "rose"
          );
        } else {
          this.notification.showNotification(
            `Unable to update user profile due to HTTP ${err.status}`,
            "rose"
          );
        }
        this.isSubmitDisabled = false;
      }
    );
  }
}
