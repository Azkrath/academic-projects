<?php

class CountryInfo
{
    private $country_info;

    function __construct()
    {
        $wsdl = "http://www.oorsprong.org/websamples.countryinfo/CountryInfoService.wso?WSDL";
        $options = array('cache_wsdl' => WSDL_CACHE_NONE,);
        $proxy = new SoapClient($wsdl, $options);
        $this->country_info = $proxy;
    }

    function getCountryISOCode($country_name)
    {
        $arg = array('sCountryName' => $country_name);
        return $this->country_info->CountryISOCode($arg)->CountryISOCodeResult;
    }

    function getCountryFlag($country_code)
    {
        $arg = array('sCountryISOCode' => $country_code);
        return $this->country_info->CountryFlag($arg)->CountryFlagResult;
    }

}