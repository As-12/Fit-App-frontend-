/* import { Injectable } from "@angular/core";
import { FitAppModule } from "../fit-app.module";

@Injectable({
  providedIn: FitAppModule,
})
export class ProgressService {
  constructor() {
  
  }

  addTodo(newTodo:Todo):Observable {
    let obs = this.todoBackendService.saveTodo(newTodo);

    obs.subscribe(
            res => {
                this._todos.next(this._todos.getValue().push(newTodo));
            });

    return obs;
}


}
 */
