import { Injectable } from "@angular/core";
import {
  BehaviorSubject,
  Observable,
  of,
  empty,
  ReplaySubject,
  throwError,
} from "rxjs";
import { User } from "../model/user.model";
import { AuthService } from "app/auth/auth.service";
import { HttpClient, HttpErrorResponse } from "@angular/common/http";
import { switchMap, map, retry, catchError } from "rxjs/operators";
import { NotificationService } from "./notification.service";

@Injectable({
  providedIn: "root",
})
export class UserService {
  private _user: ReplaySubject<User> = new ReplaySubject();

  public readonly user$: Observable<User> = this._user.asObservable();

  private _api: string = "/api/v1/users";

  constructor(
    private auth: AuthService,
    private http: HttpClient,
    private notificationService: NotificationService
  ) {
    this.auth.userProfile$
      .pipe(
        switchMap((profile) => {
          return this.getUser(profile);
        })
      )
      .subscribe((res) => {
        this._user.next(res);
      });
  }

  /*
   * Get a user from backend database.
   * If user does not exist,
   *    create one via createUser method.
   */
  public getUser(authUser: any): Observable<User> {
    let apiURL = `${this._api}/${authUser.sub}`;
    return this.http.get<User>(apiURL).pipe(
      retry(1),
      map((res) => {
        return this.mapResponse(authUser, res);
      }),
      catchError((err, caught) => {
        if (err.status === 404) {
          console.log("first login detected");
          return this.createUser(authUser);
        } else {
          return this.handleGetPostError(err);
        }
      })
    );
  }

  private createUser(authUser: any): Observable<User> {
    let apiURL = `${this._api}/`;
    let newUser: User = {
      target_weight: 0,
      height: 0,
      city: "City",
      state: "State",
    };
    return this.http.post<User>(apiURL, newUser).pipe(
      retry(1),
      map((res) => {
        return this.mapResponse(authUser, res);
      }),
      catchError((err, caught) => {
        return this.handleGetPostError(err);
      })
    );
  }

  public updateUser(updateInfo: User): Observable<User> {
    let apiURL = `${this._api}/${updateInfo.id}`;
    return this.http.patch<User>(apiURL, updateInfo).pipe(retry(1));
  }
  private handleGetPostError(err: HttpErrorResponse): Observable<User> {
    console.log(err.error);
    this.notificationService.showNotification(
      `Unable to load user profile due to code ${err.status}`
    );
    let voidUser: User = {
      target_weight: 0,
      height: 0,
      city: "Unknown",
      state: "Unknown",
    };
    return of(voidUser);
  }

  private mapResponse(authUser: any, res: User): User {
    let response: User = {
      name: authUser.name,
      id: authUser.sub,
      target_weight: res.target_weight,
      city: res.city,
      state: res.state,
      height: res.height,
    };
    return response;
  }
}
