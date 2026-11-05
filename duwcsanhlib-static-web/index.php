<?php
/**
 * DuwcsAnhLib Master Application Front Controller
 * Routes web traffic to the Unified Bookstore & Landing App
 * while preserving full WordPress admin/API access and Flatsome Theme integration.
 */
$uri = $_SERVER['REQUEST_URI'] ?? '/';

// 1. Redirect /admin and /admin/ to /wp-admin/
if ($uri === '/admin' || $uri === '/admin/' || strpos($uri, '/admin?') === 0 || strpos($uri, '/admin/') === 0) {
    header('Location: /wp-admin/', true, 301);
    exit;
}

// 2. Redirect /wp-admin without trailing slash to /wp-admin/
if ($uri === '/wp-admin' || strpos($uri, '/wp-admin?') === 0) {
    header('Location: /wp-admin/', true, 301);
    exit;
}

// 3. Allow WordPress administration, login, AJAX, REST API, cron, content requests, and Flatsome theme preview
if (
    strpos($uri, '/wp-admin') !== false ||
    strpos($uri, '/wp-login.php') !== false ||
    strpos($uri, '/wp-content') !== false ||
    strpos($uri, '/wp-includes') !== false ||
    strpos($uri, '/wp-json') !== false ||
    strpos($uri, '/xmlrpc.php') !== false ||
    strpos($uri, '/wp-cron.php') !== false ||
    isset($_GET['preview_flatsome']) ||
    isset($_GET['flatsome']) ||
    (isset($_GET['theme']) && $_GET['theme'] === 'flatsome')
) {
    define('WP_USE_THEMES', true);
    require __DIR__ . '/wp-blog-header.php';
    exit;
}

// 4. For all public bookstore & landing page traffic (root /, /?i=1, /store.html, /landing.html, etc.)
// Serve the Master Application (Keeping the user's current perfected web intact)
header('Content-Type: text/html; charset=utf-8');
header('Cache-Control: public, max-age=300');
if (file_exists(__DIR__ . '/index.html')) {
    readfile(__DIR__ . '/index.html');
    exit;
}

// Fallback to WordPress if index.html is missing
define('WP_USE_THEMES', true);
require __DIR__ . '/wp-blog-header.php';
