<?php

class GeoIP
{
    private $geo_ip;

    function __construct()
    {
        $wsdl = "http://www.webservicex.net/geoipservice.asmx?WSDL";
        $options = array('cache_wsdl' => WSDL_CACHE_NONE,);
        $proxy = new SoapClient($wsdl, $options);
        $this->geo_ip = $proxy->GetGeoIPContext()->GetGeoIPContextResult;
    }

    function getIP()
    {
        return $this->geo_ip->IP;
    }


    function getCountryName()
    {
        return $this->geo_ip->CountryName;
    }

    function getCountryCode()
    {
        return $this->geo_ip->CountryCode;
    }

}

?>