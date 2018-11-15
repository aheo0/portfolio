function jokesOnYou() {
    if (document.getElementById("joke").innerHTML == "Apollo Heo's Engineering Portfolio") {
       document.getElementById("joke").innerHTML = "You just got hacked!";
    } else {
        document.getElementById("joke").innerHTML = "Apollo Heo's Engineering Portfolio";
    }
}