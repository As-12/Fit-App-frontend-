import { Component, OnInit } from "@angular/core";
import { NotificationService } from "../services/notification.service";
import { ProgressService } from "../services/progress.service";
import { AuthService } from "app/auth/auth.service";

@Component({
  selector: "app-test-data",
  templateUrl: "./test-data.component.html",
  styleUrls: ["./test-data.component.css"],
})
export class TestDataComponent implements OnInit {
  isSubmitted: boolean = false;

  constructor(
    private notification: NotificationService,
    protected auth: AuthService,
    private progressService: ProgressService
  ) {}

  ngOnInit(): void {}

  public createTestData(user_id: string): void {
    this.isSubmitted = true;
    console.log("Submitting");

    this.progressService
      .createTestData(user_id)
      .then((res) => {
        this.notification.showNotification(
          "Test data has been generated",
          "success"
        );
        this.isSubmitted = false;
      })
      .catch((err) => {
        this.notification.showNotification(
          `Unable to generte test data due to ${err.status}`,
          "rose"
        );
      });
  }
}
