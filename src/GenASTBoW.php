<?php
require 'vendor/autoload.php';

use PhpParser\Error;
use PhpParser\ParserFactory;
// use PhpParser\NodeDumper;

function genBoW($nodes) {
    foreach($nodes as $key => $value) {
        if (gettype($value) == 'object') {
            $z = new ReflectionClass($value);
            // echo $z->getName(),' ';
            // $content = file_get_contents($filename);
            // file_put_contents($filename, $content.$z->getName().' ');
            global $words;
            $words = $words . $z->getName() . ' ';
            genBoW($value);
        } else if(is_array($value)) {
            genBoW($value);
        }
    }
}

$parser = (new ParserFactory)->create(ParserFactory::PREFER_PHP7);
$file_name = $argv[1];
$code = file_get_contents($file_name);

try {
    $stmts = $parser->parse($code);
    // var_dump($stmts);
    // $stmts is an array of statement nodes
} catch (Error $e) {
    echo 'Parse Error: ', $e->getMessage();
}

$words = '';
genBoW($stmts);
echo $words;