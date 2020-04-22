import { async, ComponentFixture, TestBed } from '@angular/core/testing';

import { FitAppComponent } from './fit-app.component';

describe('FitAppComponent', () => {
  let component: FitAppComponent;
  let fixture: ComponentFixture<FitAppComponent>;

  beforeEach(async(() => {
    TestBed.configureTestingModule({
      declarations: [ FitAppComponent ]
    })
    .compileComponents();
  }));

  beforeEach(() => {
    fixture = TestBed.createComponent(FitAppComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
