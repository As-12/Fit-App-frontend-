import { Component, OnInit } from "@angular/core";

declare const $: any;
declare interface RouteInfo {
  path: string;
  title: string;
  icon: string;
  class: string;
}
export const ROUTES: RouteInfo[] = [
  {
    path: "/fit-app/dashboard",
    title: "Dashboard",
    icon: "dashboard",
    class: "",
  },
  {
    path: "/fit-app/user-profile",
    title: "User Profile",
    icon: "person",
    class: "",
  },
  {
    path: "/fit-app/track",
    title: "Track Progress",
    icon: "content_paste",
    class: "",
  },
  {
    path: "/fit-app/history",
    title: "History",
    icon: "date_range",
    class: "",
  },
  {
    path: "/fit-app/test",
    title: "Generate Test Data",
    icon: "add_box",
    class: "",
  },
];

@Component({
  selector: "app-sidebar",
  templateUrl: "./sidebar.component.html",
  styleUrls: ["./sidebar.component.css"],
})
export class SidebarComponent implements OnInit {
  menuItems: any[];

  constructor() {}

  ngOnInit() {
    this.menuItems = ROUTES.filter((menuItem) => menuItem);
  }
  isMobileMenu() {
    if ($(window).width() > 991) {
      return false;
    }
    return true;
  }
}
