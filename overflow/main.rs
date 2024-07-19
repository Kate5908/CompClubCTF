#[macro_use] extern crate rocket;
use rocket_dyn_templates::{Template, context};

const NOTES: &'static [&'static str] = &[
    "COMPCLUB{n1ce_ov3rflow_1ll_m4ke_not3_of_i7!!}",
    "This is note number 1! Can you get to the secret note 0?",
    "This is note number 2! I used 8 bit integers in my website by the way!",
    "This is the last note! Don't have any security for the next page button... oh well!"
];

#[get("/note/<id>")]
fn note(id: u8) -> Template {
    let message = if id == 0 {
        "Hah! This note is protected"
    } else if id as usize >= NOTES.len() {
        "Note not found!"
    } else {
        NOTES[id as usize]
    };
    Template::render("index", context! { message: message, id: id })
}

#[get("/previouspage/<id>")]
fn previouspage(id: u8) -> Template {
    if (id == 0) {
        return Template::render("index", context! { message: "Hah! This note is protected", id: 0 });
    }
    let new_id = id - 1;
    let message = if new_id == 0 {
        "Hah! This note is protected"
    } else if new_id as usize >= NOTES.len() {
        "Note not found!"
    } else {
        NOTES[new_id as usize]
    };
    Template::render("index", context! { message: message, id: new_id })
}


#[get("/nextpage/<id>")]
fn nextpage(id: u8) -> Template {
    let new_id = id.overflowing_add(1).0;
    let message = if new_id as usize >= NOTES.len() {
        "Note not found!"
    } else {
        NOTES[new_id as usize]
    };
    Template::render("index", context! { message: message, id: new_id })
}

#[launch]
fn rocket() -> _ {
    rocket::build()
        .mount("/", routes![note, previouspage, nextpage])
        .attach(Template::fairing())
}