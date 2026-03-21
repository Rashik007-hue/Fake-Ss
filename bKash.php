<?php
header('Content-Type: image/png');

// URL থেকে ইনপুট নেওয়া হচ্ছে
$number = isset($_GET['number']) ? htmlspecialchars($_GET['number']) : '01986833907';
$transactionId = isset($_GET['transaction']) ? htmlspecialchars($_GET['transaction']) : '730MGQG6GH';
$amount = isset($_GET['amount']) ? (int) htmlspecialchars($_GET['amount']) : 10000;

$total = $amount;
$totalWithExtra = $total + 17;

date_default_timezone_set('Asia/Dhaka');
$time = date('h:i A');
$dayMonthYear = date('d/m/y');

$backgroundPath = __DIR__ . '/ss.jpg';
if (!file_exists($backgroundPath)) {
    die('Error: Background image not found.');
}

$background = imagecreatefromjpeg($backgroundPath);
$black = imagecolorallocate($background, 90, 90, 90);
$black2 = imagecolorallocate($background, 90, 90, 90);

$fontPath1 = __DIR__ . '/roboto.ttf';
$fontPath2 = __DIR__ . '/roboto2.ttf';

if (!file_exists($fontPath1) || !file_exists($fontPath2)) {
    die('Error: Font file(s) missing.');
}

$fontSize = 50;
$fontSizeBold = 55;
$fontSizeBold2 = 60;
$trim = 47;
$imageWidth = imagesx($background);

$textStyles = [
    'number1' => ['x' => 400, 'y' => 850, 'size' => $fontSizeBold, 'font' => $fontPath1, 'color' => $black],
    'number2' => ['x' => 400, 'y' => 950, 'size' => $fontSizeBold, 'font' => $fontPath2, 'color' => $black],
    'transactionId' => ['x' => $imageWidth - 384, 'y' => 1430, 'size' => $fontSizeBold2, 'font' => $fontPath1, 'color' => $black, 'align' => 'right'],
    'total' => ['x' => 175, 'y' => 1880, 'size' => $fontSize, 'font' => $fontPath2, 'color' => $black],
    'totalWithExtra' => ['x' => 170, 'y' => 1768, 'size' => $fontSize, 'font' => $fontPath1, 'color' => $black2],
    'time' => ['x' => 135, 'y' => 1421, 'size' => $fontSize, 'font' => $fontPath1, 'color' => $black],
    'dayMonthYear' => ['x' => 439, 'y' => 1420, 'size' => $fontSize, 'font' => $fontPath1, 'color' => $black],
    'timeeee' => ['x' => 50, 'y' => 109, 'size' => $trim, 'font' => $fontPath2, 'color' => $black],
];

$texts = [
    'number1' => $number,
    'number2' => $number,
    'transactionId' => $transactionId,
    'total' => $total . ' +17.39',
    'totalWithExtra' => $totalWithExtra,
    'time' => $time,
    'dayMonthYear' => $dayMonthYear,
    'timeeee' => $time
];

foreach ($textStyles as $key => $style) {
    if (isset($texts[$key])) {
        $x = $style['x'];
        if (isset($style['align']) && $style['align'] == 'right') {
            $bbox = imagettfbbox($style['size'], 0, $style['font'], $texts[$key]);
            $textWidth = abs($bbox[2] - $bbox[0]);
            $x = $style['x'] - $textWidth;
        }
        imagettftext($background, $style['size'], 0, $x, $style['y'], $style['color'], $style['font'], $texts[$key]);
    }
}

imagepng($background);
imagedestroy($background);
?>