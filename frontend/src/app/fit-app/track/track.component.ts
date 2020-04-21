import { Component, OnInit } from "@angular/core";
import { ProgressService } from "../services/progress.service";
import { Progress } from "../model/progress.model";
import { DatePipe } from "@angular/common";
import { NgForm } from "@angular/forms";
import { NotificationService } from "../services/notification.service";
import { UserService } from "../services/user.service";

declare interface radioImage {
  image: string;
  value: string;
}

@Component({
  selector: "app-track",
  templateUrl: "./track.component.html",
  styleUrls: ["./track.component.css"],
})
export class TrackComponent implements OnInit {
  protected today: Date = new Date();
  protected isSubmitted: Boolean = false;

  protected progress: Progress;

  moods: radioImage[] = [
    {
      image: "./assets/img/sad-face.svg",
      value: "bad",
    },
    {
      image: "./assets/img/neutral-face.svg",
      value: "neutral",
    },

    {
      image: "./assets/img/happy-face.svg",
      value: "good",
    },
  ];

  constructor(
    private progressService: ProgressService,
    private userService: UserService,
    private datePipe: DatePipe,
    private notification: NotificationService
  ) {}

  ngOnInit(): void {
    this.userService.user$.subscribe((res) => {
      this.progress = {
        track_date: this.datePipe.transform(this.today, "yyyy-MM-dd"),
        user_id: res.id,
        weight: 0,
        mood: "neutral",
        diet: "neutral",
      };
    });
  }

  validateData() {
    //Bugfix: Ngmodel binding seems to cast the number to string
    this.progress.weight = +this.progress.weight;
  }

  trackWeight(form: NgForm): void {
    this.isSubmitted = true;
    console.log("Submitting");
    this.validateData();
    this.progressService.trackProgress(this.progress).subscribe(
      (res) => {
        this.notification.showNotification(
          "Progress has been submitted",
          "success"
        );
        this.isSubmitted = false;
      },
      (err) => {
        if (err.status === 400 || err.status === 422) {
          this.notification.showNotification(
            `You can only submit one progress per day`,
            "rose"
          );
        } else {
          this.notification.showNotification(
            `Unable to update user profile due to HTTP ${err.status}`,
            "rose"
          );
        }
        this.isSubmitted = false;
      }
    );
  }
}
