/*
 * Hola mundo para New 3DS con SDL2.
 *
 * Qué demuestra:
 *   - La toolchain funciona (devkitARM + libctru + SDL2).
 *   - Un bucle principal con vsync en la pantalla de arriba (400x240).
 *   - Entrada: el Circle Pad mueve el cuadro, START sale.
 *   - Medición: FPS y milisegundos por cuadro, dibujados con una fuente
 *     de 3x5 píxeles hecha a mano (no hace falta SDL_ttf).
 */
#include <SDL2/SDL.h>
#include <stdio.h>
#ifdef __3DS__
#include <3ds.h>
#endif

#define SCREEN_W 400
#define SCREEN_H 240
#define BOX_SIZE 32
#define BOX_SPEED 4
#define PIXEL 4 /* tamaño en pantalla de cada píxel de la fuente */

/* Dígitos 0-9 y el punto, en filas de 3 bits (bit 2 = columna izquierda). */
static const Uint8 FONT[11][5] = {
    {7, 5, 5, 5, 7}, {2, 6, 2, 2, 7}, {7, 1, 7, 4, 7}, {7, 1, 7, 1, 7},
    {5, 5, 7, 1, 1}, {7, 4, 7, 1, 7}, {7, 4, 7, 5, 7}, {7, 1, 1, 1, 1},
    {7, 5, 7, 5, 7}, {7, 5, 7, 1, 7}, {0, 0, 0, 0, 2},
};

static void draw_text(SDL_Renderer *r, const char *text, int x, int y)
{
    for (; *text; text++, x += 4 * PIXEL) {
        int glyph;
        if (*text >= '0' && *text <= '9')
            glyph = *text - '0';
        else if (*text == '.')
            glyph = 10;
        else
            continue; /* espacios y otros caracteres solo avanzan */

        for (int row = 0; row < 5; row++)
            for (int col = 0; col < 3; col++)
                if (FONT[glyph][row] & (4 >> col)) {
                    SDL_Rect px = {x + col * PIXEL, y + row * PIXEL, PIXEL, PIXEL};
                    SDL_RenderFillRect(r, &px);
                }
    }
}

int main(int argc, char *argv[])
{
    (void)argc;
    (void)argv;

    if (SDL_Init(SDL_INIT_VIDEO | SDL_INIT_GAMECONTROLLER) != 0) {
        printf("SDL_Init: %s\n", SDL_GetError());
        return 1;
    }

    SDL_Window *window = SDL_CreateWindow("hello_n3ds", SDL_WINDOWPOS_UNDEFINED,
                                          SDL_WINDOWPOS_UNDEFINED, SCREEN_W,
                                          SCREEN_H, 0);
    SDL_Renderer *renderer = SDL_CreateRenderer(window, -1, SDL_RENDERER_PRESENTVSYNC);
    SDL_GameController *pad = SDL_GameControllerOpen(0);

    if (!window || !renderer) {
        printf("Ventana o renderer: %s\n", SDL_GetError());
        SDL_Quit();
        return 1;
    }

    int box_x = (SCREEN_W - BOX_SIZE) / 2;
    int box_y = (SCREEN_H - BOX_SIZE) / 2;

    /* Se promedia cada medio segundo para que los números no parpadeen. */
    Uint64 freq = SDL_GetPerformanceFrequency();
    Uint64 window_start = SDL_GetPerformanceCounter();
    int frames = 0;
    char fps_text[16] = "0";
    char ms_text[16] = "0";

    int running = 1;
    while (running) {
        SDL_Event e;
        while (SDL_PollEvent(&e)) {
            if (e.type == SDL_QUIT)
                running = 0;
            if (e.type == SDL_CONTROLLERBUTTONDOWN &&
                e.cbutton.button == SDL_CONTROLLER_BUTTON_START)
                running = 0;
        }

        if (pad) {
            /* Zona muerta para que el Circle Pad no deslice solo. */
            Sint16 ax = SDL_GameControllerGetAxis(pad, SDL_CONTROLLER_AXIS_LEFTX);
            Sint16 ay = SDL_GameControllerGetAxis(pad, SDL_CONTROLLER_AXIS_LEFTY);
            if (ax > 8000 || ax < -8000)
                box_x += ax > 0 ? BOX_SPEED : -BOX_SPEED;
            if (ay > 8000 || ay < -8000)
                box_y += ay > 0 ? BOX_SPEED : -BOX_SPEED;
        }
        if (box_x < 0) box_x = 0;
        if (box_y < 0) box_y = 0;
        if (box_x > SCREEN_W - BOX_SIZE) box_x = SCREEN_W - BOX_SIZE;
        if (box_y > SCREEN_H - BOX_SIZE) box_y = SCREEN_H - BOX_SIZE;

        SDL_SetRenderDrawColor(renderer, 16, 16, 24, 255);
        SDL_RenderClear(renderer);

        SDL_SetRenderDrawColor(renderer, 230, 60, 60, 255);
        SDL_Rect box = {box_x, box_y, BOX_SIZE, BOX_SIZE};
        SDL_RenderFillRect(renderer, &box);

        SDL_SetRenderDrawColor(renderer, 240, 240, 240, 255);
        draw_text(renderer, fps_text, 8, 8);           /* FPS */
        draw_text(renderer, ms_text, 8, 8 + 7 * PIXEL); /* ms por cuadro */

        SDL_RenderPresent(renderer);
#ifdef __3DS__
        /* SDL2 para 3DS ignora SDL_RENDERER_PRESENTVSYNC: sin esto el bucle
         * corría a ~108 FPS en una New 3DS. Se espera el refresco a mano. */
        gspWaitForVBlank();
#endif

        frames++;
        Uint64 now = SDL_GetPerformanceCounter();
        double elapsed = (double)(now - window_start) / (double)freq;
        if (elapsed >= 0.5) {
            snprintf(fps_text, sizeof fps_text, "%.1f", frames / elapsed);
            snprintf(ms_text, sizeof ms_text, "%.2f", elapsed * 1000.0 / frames);
            frames = 0;
            window_start = now;
        }
    }

    if (pad)
        SDL_GameControllerClose(pad);
    SDL_DestroyRenderer(renderer);
    SDL_DestroyWindow(window);
    SDL_Quit();
    return 0;
}
