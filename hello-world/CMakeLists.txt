cmake_minimum_required(VERSION 3.13)
project(hello_n3ds C)

set(CMAKE_C_STANDARD 99)

add_executable(hello_n3ds source/main.c)
target_compile_options(hello_n3ds PRIVATE -Wall -Wextra -O2)

find_package(SDL2 REQUIRED)
# Los portlibs de 3DS solo traen SDL2 estático; según la versión, el
# target se llama SDL2::SDL2 o SDL2::SDL2-static.
if(TARGET SDL2::SDL2)
    set(SDL2_TARGET SDL2::SDL2)
else()
    set(SDL2_TARGET SDL2::SDL2-static)
endif()
if(TARGET SDL2::SDL2main)
    target_link_libraries(hello_n3ds PRIVATE SDL2::SDL2main)
endif()
target_link_libraries(hello_n3ds PRIVATE ${SDL2_TARGET})

# Genera el .3dsx que abre el Homebrew Launcher (función del toolchain de devkitPro).
ctr_create_3dsx(hello_n3ds)
