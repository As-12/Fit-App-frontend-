import { Component, OnInit } from "@angular/core";
import { ProgressService } from "../services/progress.service";

@Component({
  selector: "app-history",
  templateUrl: "./history.component.html",
  styleUrls: ["./history.component.css"],
})
export class HistoryComponent implements OnInit {
  constructor(public progressService: ProgressService) {}

  ngOnInit(): void {
    this.progressService.progress$.subscribe((res) => {
      console.log(res);
    });
  }
}
