import { Injectable } from "@angular/core";
import {
  Observable,
  of,
  ReplaySubject,
  BehaviorSubject,
  throwError,
  empty,
} from "rxjs";
import { User } from "../model/user.model";
import { AuthService } from "app/auth/auth.service";
import { HttpClient, HttpErrorResponse } from "@angular/common/http";
import { switchMap, map, retry, catchError } from "rxjs/operators";
import { NotificationService } from "./notification.service";
import { UserService } from "./user.service";
import { ProgressList, Progress } from "../model/progress.model";

@Injectable({
  providedIn: "root",
})
export class ProgressService {
  private _progress: BehaviorSubject<ProgressList> = new BehaviorSubject(null);

  public readonly progress$: Observable<
    ProgressList
  > = this._progress.asObservable();

  private _api: string = "/api/v1/progress";
  public user_id: string = "";

  constructor(
    private auth: AuthService,
    private userService: UserService,
    private http: HttpClient,
    private notificationService: NotificationService
  ) {
    this.userService.user$
      .pipe(
        switchMap((user) => {
          this.user_id = user.id;
          return this.get_user_progress();
        })
      )
      .subscribe((res) => {
        console.log(`${this.user_id} progress has been loaded`);
      });
  }

  public get_user_progress(): Observable<ProgressList> {
    if (this.user_id === "") {
      return throwError(
        "Oop! it looks like user profile has not been fully loaded"
      );
    }
    let apiURL = `${this._api}/${this.user_id}`;
    return this.http.get<ProgressList>(apiURL).pipe(
      retry(1),
      map((res) => {
        return this.mapResponse(res);
      })
    );
  }

  public trackProgress(progress: Progress): Observable<Progress> {
    if (this.user_id === "") {
      return throwError(
        "Oop! it looks like user profile has not been fully loaded"
      );
    }
    let apiURL = `${this._api}/${this.user_id}`;
    return this.http.post<Progress>(apiURL, progress).pipe(
      retry(1),
      map((resp) => {
        let currentList = this._progress.getValue().progresses;
        currentList.push(resp);
        let newValue: ProgressList = {
          user_id: this.user_id,
          progresses: currentList,
          count: currentList.length,
        };
        this._progress.next(newValue);
        return resp;
      })
    );
  }

  private mapResponse(res: ProgressList): ProgressList {
    let response: ProgressList = {
      user_id: res.user_id,
      progresses: res.progresses,
      count: res.count,
    };
    this._progress.next(response);
    return response;
  }

  public createTestData(): Observable<ProgressList> {
    if (this.user_id === "") {
      return throwError(
        "Oop! it looks like user profile has not been fully loaded"
      );
    }
    let apiURL = `${this._api}/test/${this.user_id}`;
    return this.http.get<any>(apiURL).pipe(
      map((res) => {
        return this.mapResponse(res);
      })
    );
  }
}
