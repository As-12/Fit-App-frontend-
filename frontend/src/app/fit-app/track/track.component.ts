import { Component, OnInit } from "@angular/core";

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
  today: Date = new Date();
  isSubmitted: Boolean = false;

  public submitForm(): void {
    this.isSubmitted = true;
  }
  moods: radioImage[] = [
    {
      image: "./assets/img/sad-face.svg",
      value: "-1",
    },
    {
      image: "./assets/img/neutral-face.svg",
      value: "0",
    },

    {
      image: "./assets/img/happy-face.svg",
      value: "1",
    },
  ];

  constructor() {}

  ngOnInit(): void {}
}
