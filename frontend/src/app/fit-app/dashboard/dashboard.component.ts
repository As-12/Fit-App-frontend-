import { Component, OnInit } from "@angular/core";
import * as Chartist from "chartist";
import { ProgressService } from "../services/progress.service";
import { ProgressList, Progress } from "../model/progress.model";
import { DatePipe } from "@angular/common";
import { UserService } from "../services/user.service";
import { AuthService } from "app/auth/auth.service";

@Component({
  selector: "app-dashboard",
  templateUrl: "./dashboard.component.html",
  styleUrls: ["./dashboard.component.css"],
})
export class DashboardComponent implements OnInit {
  constructor(
    private auth: AuthService,
    private userService: UserService,
    private progressService: ProgressService,
    private datePipe: DatePipe
  ) {}
  startAnimationForLineChart(chart) {
    let seq: any, delays: any, durations: any;
    seq = 0;
    delays = 80;
    durations = 500;

    chart.on("draw", function (data) {
      if (data.type === "line" || data.type === "area") {
        data.element.animate({
          d: {
            begin: 600,
            dur: 700,
            from: data.path
              .clone()
              .scale(1, 0)
              .translate(0, data.chartRect.height())
              .stringify(),
            to: data.path.clone().stringify(),
            easing: Chartist.Svg.Easing.easeOutQuint,
          },
        });
      } else if (data.type === "point") {
        seq++;
        data.element.animate({
          opacity: {
            begin: seq * delays,
            dur: durations,
            from: 0,
            to: 1,
            easing: "ease",
          },
        });
      }
    });

    seq = 0;
  }
  startAnimationForBarChart(chart) {
    let seq2: any, delays2: any, durations2: any;

    seq2 = 0;
    delays2 = 80;
    durations2 = 500;
    chart.on("draw", function (data) {
      if (data.type === "bar") {
        seq2++;
        data.element.animate({
          opacity: {
            begin: seq2 * delays2,
            dur: durations2,
            from: 0,
            to: 1,
            easing: "ease",
          },
        });
      }
    });

    seq2 = 0;
  }
  ngOnInit() {
    //Load chart once the user has been loaded.
    this.userService.user$.subscribe((res) => this.createDailyProgressChart());
    this.userService.user$.subscribe((res) =>
      this.createDailyNetProgressChart(res.target_weight)
    );
  }

  createDailyProgressChart(): void {
    this.progressService.get_user_progress().subscribe((res) => {
      let series: number[] = [];
      let labels: string[] = [];
      let maxVal: number = 0;
      for (let i = 0; i != res.progresses.length && i < 7; ++i) {
        let progress: Progress = res.progresses[i];
        let date: string = this.datePipe.transform(progress.track_date, "M/d");
        if (maxVal < progress.weight) maxVal = progress.weight;
        series.push(progress.weight);
        labels.push(date);
      }

      const dataProgress: any = {
        labels: labels.reverse(),
        series: [series.reverse()],
      };

      const optionsDailyProgressChart: any = {
        lineSmooth: Chartist.Interpolation.cardinal({
          tension: 0,
        }),
        low: 0,
        high: maxVal * 1.2,
        chartPadding: { top: 0, right: 0, bottom: 0, left: 0 },
      };

      var dailySalesChart = new Chartist.Line(
        "#dailyProgressChart",
        dataProgress,
        optionsDailyProgressChart
      );
      this.startAnimationForLineChart(dailySalesChart);
    });
  }

  createDailyNetProgressChart(target_weight: number): void {
    this.progressService.get_user_progress().subscribe((res) => {
      let series: number[] = [];
      let labels: string[] = [];
      let maxVal: number = 0;
      let minVal: number = 0;
      for (let i = 0; i != res.progresses.length && i < 7; ++i) {
        let progress: Progress = res.progresses[i];
        let date: string = this.datePipe.transform(progress.track_date, "M/d");
        let progress_val = progress.weight - target_weight;
        if (maxVal < progress_val) maxVal = progress_val;
        if (minVal > progress_val) minVal = progress_val;
        series.push(progress_val);
        labels.push(date);
      }

      const dataNetProgress: any = {
        labels: labels.reverse(),
        series: [series.reverse()],
      };

      var optionsProgressChart = {
        axisX: {
          showGrid: false,
        },
        low: minVal,
        high: maxVal + 10,
        chartPadding: { top: 0, right: 5, bottom: 0, left: 0 },
      };

      var responsiveOptions: any[] = [
        [
          "screen and (max-width: 640px)",
          {
            seriesBarDistance: 5,
            axisX: {
              labelInterpolationFnc: function (value) {
                return value[0];
              },
            },
          },
        ],
      ];
      var netProgressChart = new Chartist.Bar(
        "#netProgressChart",
        dataNetProgress,
        optionsProgressChart,
        responsiveOptions
      );
      this.startAnimationForBarChart(netProgressChart);
    });
  }
}
