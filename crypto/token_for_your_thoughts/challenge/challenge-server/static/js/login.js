function onInputKeyUp(e) {
    e.preventDefault();
    if (e.keyCode === 13)  // Enter
    {
        $("#login").click();
    }
}

function showError(msg) {
    $("#alert-reason").text(msg);
    $("#alert").fadeIn();
}

function closeError() {
    $("#alert").fadeOut();    
}

function disableInput(disabled) {
    $("#username").prop("disabled", disabled);
    $("#token").prop("disabled", disabled);
    $("#login").prop("disabled", disabled);
}

$(document).ready(function() {
    particlesJS("particles-js", {
        "particles": {
            "number": {
                "value": 80,
                "density": {
                    "enable": false,
                    "value_area": 1200
                }
            },
            "color": {
                "value": "#ffffff"
            },
            "shape": {
                "type": "circle",
                "stroke": {
                    "width": 0,
                    "color": "#000000"
                },
                "polygon": {
                    "nb_sides": 5
                },
                "image": {
                    "src": "img/github.svg",
                    "width": 100,
                    "height": 100
                }
            },
            "opacity": {
                "value": 0.5,
                "random": true,
                "anim": {
                    "enable": false,
                    "speed": 1,
                    "opacity_min": 0.1,
                    "sync": false
                }
            },
            "size": {
                "value": 1,
                "random": true,
                "anim": {
                    "enable": false,
                    "speed": 40,
                    "size_min": 0.1,
                    "sync": false
                }
            },
            "line_linked": {
                "enable": true,
                "distance": 250,
                "color": "#ffffff",
                "opacity": 0.4,
                "width": 1
            },
            "move": {
                "enable": true,
                "speed": 1.5,
                "direction": "none",
                "random": true,
                "straight": false,
                "out_mode": "out",
                "bounce": false,
                "attract": {
                    "enable": false,
                    "rotateX": 600,
                    "rotateY": 1200
                }
            }
        },
        "interactivity": {
            "detect_on": "canvas",
            "events": {
                "onhover": {
                    "enable": true,
                    "mode": "grab"
                },
                "onclick": {
                    "enable": false,
                    "mode": "push"
                },
                "resize": true
            },
            "modes": {
                "grab": {
                    "distance": 100,
                    "line_linked": {
                        "opacity": 0.5
                    }
                },
                "bubble": {
                    "distance": 400,
                    "size": 40,
                    "duration": 2,
                    "opacity": 8,
                    "speed": 3
                },
                "repulse": {
                    "distance": 200,
                    "duration": 0.4
                },
                "push": {
                    "particles_nb": 4
                },
                "remove": {
                    "particles_nb": 2
                }
            }
        },
        "retina_detect": true
    });

    $("#username").keyup(onInputKeyUp);
    $("#token").keyup(onInputKeyUp);

    $.ajaxSetup({
        type: "POST",
        timeout: 5000
    });

    $("#login").click(function() {
        var req = {
            username: $("#username").val(),
            token: $("#token").val()
        };

        disableInput(true);
        $.post('/login', req, function(res) {
            disableInput(false);
            if (!res.success) {
                showError(res.msg);
            } else {
                closeError();
                $("#logo").text(res.msg);
                $("#logo").css("transform", "none");
                $("#logo").css("font-size", "3em");
                $("#logo").css("padding-top", "8px");
            }
        }).fail(function(xhr, status, error) {
            showError("The request was unsuccessful. Check your network connection.");
        });;
    });

    $("#close-alert").click(closeError);
});
