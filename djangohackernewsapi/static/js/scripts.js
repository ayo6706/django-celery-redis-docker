const csrftoken = $("[name=csrfmiddlewaretoken]").val();
const types = document.querySelectorAll("li input[type=radio]");
const postSearchBox = document.getElementById("storySearchBox");
const loader = `<div class="border border-solid border-gray-400 shadow    rounded-md p-4 max-w-full w-full mx-auto storyLoader">
<div class="animate-pulse flex space-x-4">
  <div class="rounded-none bg-gray-400 h-20 w-6"></div>
  <div class="flex-1 space-y-4 py-1">
    <div class="h-4 bg-gray-400 rounded w-2/6"></div>
    <div class="space-y-2">
      <div class="h-4 bg-gray-400 rounded w-5/6"></div>
      <div class="h-4 bg-gray-400 rounded w-1/6"></div>
    </div>
  </div>
</div>
</div>`;
const isEmpty = (el) => {
    return !$.trim(el.html());
};
if (csrftoken) {
    function csrfSafeMethod(method) {
        // these HTTP methods do not require CSRF protection
        return /^(GET|HEAD|OPTIONS|TRACE)$/.test(method);
    }
    $.ajaxSetup({
        beforeSend: function (xhr, settings) {
            if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
                xhr.setRequestHeader("X-CSRFToken", csrftoken);
            }
            if (isEmpty($("#hackerNewsStories"))) {
                for (let index = 0; index < 4; index++) {
                    $("#hackerNewsStories").html(loader);
                }
            } else {
                $("#hackerNewsStories").append(loader);
            }
        },
        complete: function () {
            $(".storyLoader").fadeOut();
        },
    });
}

$("#lazyLoadLink").on("click", function () {
    let link = $(this);
    let page = link.data("page");
    $.ajax({
        type: "POST",
        url: "/lazy_load_posts/", //"{% url 'news:lazy_load_posts' %}",
        data: {
            page: page,
        },
        success: function (response) {
            // if there are still more pages to load,
            // add 1 to the "Load More posts" link's page data attribute
            // else hide the link
            if (response.has_next) {
                link.data("page", page + 1);
            } else {
                link.fadeOut();
            }
            // append html to the posts div
            $("#stories").append(response.posts_html);
            $("#storiesCount").html(
                parseInt($("#storiesCount").text(), 10) + response.posts_count
            );
        },
        error: function (xhr, status, error) {
            console.error(xhr, status, error);
        },
    });
});

types.forEach((radioElement) => {
    radioElement.addEventListener("click", (event) => {
        console.log(event.target.value);
        filterPost(event.target.value);
    });
});
const filterPost = (value) => {
    let link = document.getElementById("lazyLoadLink");
    let page = link.dataset.page;
    let formData = new FormData();
    formData.append("post_type", value);
    formData.append("page", page);
    $.ajax({
        url: "/filter_by_story_type/",
        type: "POST",
        dataType: "json",
        cache: false,
        processData: false,
        contentType: false,
        data: formData,
        error: function (xhr) {
            console.error(xhr.statusText);
        },
        success: (response) => {
            if (response.no_post) {
                $("#storiesCount").html(0);
                $("#stories")
                    .html(`<div class="border border-solid border-gray-400 bg-white rounded shadow flex mb-2 p-2 text-center">
                  <p class="text-2xl font-bold text-center">
                    No latest post for the filter ${value}
                  </p>
                </div>`);
                $("#lazyLoadLink").fadeOut();
            } else {
                $("#stories").html(response.posts_html);
                $("#storiesCount").html(0 + response.posts_count);
                if (response.has_next) {
                    // $("#lazyLoadLink").fadeIn();
                    $("#lazyLoadLink").hide();
                    let newpage = 1;
                    let empty_page = false;
                    let block_request = false;

                    $(window).scroll(function () {
                        let margin =
                            $(document).height() - $(window).height() - 200;
                        if (
                            $(window).scrollTop() > margin &&
                            empty_page == false &&
                            block_request == false
                        ) {
                            block_request = true;
                            newpage += 1;
                            $.get(
                                `/filter_by_story_type/?page=${newpage}&post_type=${value}`,
                                (data) => {
                                    if (data.newhas_next) {
                                        block_request = false;
                                        $("#stories").append(
                                            data.newposts_html
                                        );
                                        $("#storiesCount").html(
                                            parseInt(
                                                $("#storiesCount").text(),
                                                10
                                            ) + +data.newposts_count
                                        );
                                    } else {
                                        empty_page = true;
                                    }
                                }
                            );
                        }
                    });
                } else {
                    $("#lazyLoadLink").fadeOut();
                }
            }
        },
    });
};

storySearchBox.addEventListener("keyup", (event) => {
    let link = document.getElementById("lazyLoadLink");
    let page = link.dataset.page;
    let formData = new FormData();
    formData.append("search_text", event.target.value);
    formData.append("page", page);
    $.ajax({
        url: "/search_by_text/",
        type: "POST",
        dataType: "json",
        cache: false,
        processData: false,
        contentType: false,
        data: formData,
        error: function (xhr) {
            console.error(xhr.statusText);
        },
        success: (response) => {
            if (response.no_post) {
                $("#storiesCount").html(0);
                $("#stories")
                    .html(`<div class="border border-solid border-gray-400 bg-white rounded shadow flex mb-2 p-2">
              <p class="text-2xl font-bold text-center">
                No latest post for your query, ${event.target.value}.
              </p>
            </div>`);
                $("#lazyLoadLink").fadeOut();
            } else {
                $("#stories").html(response.posts_html);
                $("#storiesCount").html(0 + response.posts_count);
                let context = document.querySelector("#stories");
                let instance = new Mark(context);
                instance.mark(event.target.value, {
                    element: "span",
                    className: "highlight",
                });
                if (response.has_next) {
                    $("#lazyLoadLink").hide();
                    let newpage = 1;
                    let empty_page = false;
                    let block_request = false;

                    $(window).scroll(function () {
                        let margin =
                            $(document).height() - $(window).height() - 200;
                        if (
                            $(window).scrollTop() > margin &&
                            empty_page == false &&
                            block_request == false
                        ) {
                            block_request = true;
                            newpage += 1;
                            $.get(
                                `/search_by_text/?page=${newpage}&search_text=${event.target.value}`,
                                (data) => {
                                    if (data.newhas_next) {
                                        block_request = false;
                                        $("#stories").append(
                                            data.newposts_html
                                        );
                                        $("#storiesCount").html(
                                            parseInt(
                                                $("#storiesCount").text(),
                                                10
                                            ) + +data.newposts_count
                                        );
                                    } else {
                                        empty_page = true;
                                    }
                                }
                            );
                        }
                    });
                } else {
                    $("#lazyLoadLink").fadeOut();
                }
            }
        },
    });
});

if (document.querySelector("#latestStoryEmpty")) {
    $("#lazyLoadLink").hide();
} else {
    $("#lazyLoadLink").fadeIn();
}

// function setTheme(themeName) {
//     localStorage.setItem("theme", themeName);
//     document.getElementById("checkbox").checked = true;
//     localStorage.setItem("themeSwitcher", "true");
//     document.documentElement.classList.add(themeName);
// }

// function removeTheme(themeName) {
//     document.documentElement.classList.remove(themeName);
//     localStorage.setItem("theme", "");
//     document.getElementById("checkbox").checked = false;
//     localStorage.setItem("themeSwitcher", "false");
// }
// // function to toggle between light and dark theme
// function toggleTheme() {
//     if (localStorage.getItem("theme") === "dark") {
//         removeTheme("dark");
//     } else {
//         setTheme("dark");
//     }
// }
// // Immediately invoked function to set the theme on initial load
// (function () {
//     if (localStorage.getItem("theme") === "dark") {
//         setTheme("dark");
//     } else {
//         removeTheme("dark");
//     }
// })();
