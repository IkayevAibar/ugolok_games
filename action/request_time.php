<?php

$curl = curl_init();

curl_setopt_array($curl, array(
  CURLOPT_URL => 'https://timercheck.io/ugolok-timer',
  CURLOPT_RETURNTRANSFER => true,
  CURLOPT_ENCODING => '',
  CURLOPT_MAXREDIRS => 10,
  CURLOPT_TIMEOUT => 0,
  CURLOPT_FOLLOWLOCATION => true,
  CURLOPT_HTTP_VERSION => CURL_HTTP_VERSION_1_1,
  CURLOPT_CUSTOMREQUEST => 'GET',
  CURLOPT_HTTPHEADER => array(
    'Access-Control-Allow-Headers: Content-Type',
    'Access-Control-Allow-Origin: *',
    'Access-Control-Allow-Methods: OPTIONS,POST,GET'
  ),
));

$response = curl_exec($curl);

curl_close($curl);
echo $response;

?>