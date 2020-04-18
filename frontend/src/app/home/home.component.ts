import { Component, OnInit, ViewChild } from "@angular/core";
import { AuthService } from "../auth/auth.service";

@Component({
  selector: "app-home",
  templateUrl: "./home.component.html",
  styleUrls: ["./home.component.css"],
})
export class HomeComponent implements OnInit {
  constructor(private auth: AuthService) {}
  today: Date = new Date();
  ngOnInit(): void {}

  @ViewChild("myVideo") myVideo: any;

  afterViewInit() {
    let video: HTMLVideoElement = <HTMLVideoElement>this.myVideo.nativeElement;
    video.play();
  }
}
