import { Component, OnInit } from "@angular/core";

declare interface radioImage {
  image: string;
  value: string;
}

@Component({
  selector: "app-edit",
  templateUrl: "./edit.component.html",
  styleUrls: ["./edit.component.css"],
})
export class EditComponent implements OnInit {
  constructor() {}

  ngOnInit(): void {}

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
}
