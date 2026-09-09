<?php

use Illuminate\Http\Request;
use Illuminate\Support\Facades\Route;

Route::get('/health', function () {
    return response()->json(['status' => 'ok']);
});

Route::get('/tasks', function () {
    return response()->json(cache('tasks', []));
});

Route::post('/tasks', function (Request $request) {
    $tasks = cache('tasks', []);
    $task = [
        'id' => count($tasks) + 1,
        'title' => $request->input('title'),
        'done' => false,
    ];
    $tasks[] = $task;
    cache(['tasks' => $tasks], now()->addHours(1));
    return response()->json($task, 201);
});
