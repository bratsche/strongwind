<?xml version="1.0" encoding="UTF-8"?>
<xsl:stylesheet version="1.0" xmlns:xsl="http://www.w3.org/1999/XSL/Transform">
<xsl:template match="/">
  <html lang="en">
    <head>
      <title><xsl:value-of select="test/name"/></title>
      <link rel="stylesheet" type="text/css" href="procedures.css" media="all"/>
    </head>
    <body>
      <p class="header">
        <a href="http://www.medsphere.org/projects/strongwind"><img src="strongwind.png" width="182" height="172" alt="Strongwind"/></a><br/><br/>
        <span id="testName"><xsl:value-of select="test/name"/></span><br/>
        <span id="documentName">Strongwind Test Script</span><br/>
        <span id="testDescription"><xsl:value-of select="test/description"/></span><br/>
        <xsl:comment>Convert the number of seconds it took the test to run into
        days, hours, minutes, and seconds</xsl:comment>
        <xsl:variable name="numDays" select="floor(number(test/time) div 86400)"/>
        <xsl:variable name="tmpSec1" select="number(test/time) mod 86400"/>
        <xsl:variable name="numHours" select="floor($tmpSec1 div 3600)"/>
        <xsl:variable name="tmpSec2" select="$tmpSec1 mod 3600"/>
        <xsl:variable name="numMinutes" select="floor($tmpSec2 div 60)"/>
        <xsl:variable name="numSeconds" select="format-number(number(test/time) mod 60, '#.#')"/>
        <xsl:comment>Finished converting</xsl:comment>
        <span id="testTimeText">Estimated Run Time: </span>
        <xsl:if test="$numDays > 0">
            <span id="days"><xsl:value-of select="$numDays"/></span>
          <xsl:choose>
            <xsl:when test="$numDays = 1">
              <span id="timeDays"> Day</span>
            </xsl:when>
            <xsl:otherwise>
              <span id="timeDays"> Days</span>
            </xsl:otherwise>
          </xsl:choose>
          <xsl:if test="($numHours > 0) or ($numMinutes > 0) or ($numSeconds > 0)">
            <span>, </span>
          </xsl:if>
        </xsl:if>
        <xsl:if test="$numHours > 0">
            <span id="hours"><xsl:value-of select="$numHours"/></span>
          <xsl:choose>
            <xsl:when test="$numHours = 1">
              <span id="timeHours"> Hour</span>
            </xsl:when>
            <xsl:otherwise>
              <span id="timeHours"> Hours</span>
            </xsl:otherwise>
          </xsl:choose>
          <xsl:if test="($numMinutes > 0) or ($numSeconds > 0)">
            <span>, </span>
          </xsl:if>
        </xsl:if>
        <xsl:if test="$numMinutes > 0">
            <span id="minutes"><xsl:value-of select="$numMinutes"/></span>
          <xsl:choose>
            <xsl:when test="$numMinutes = 1">
              <span id="timeMinutes"> Minute</span>
            </xsl:when>
            <xsl:otherwise>
              <span id="timeMinutes"> Minutes</span>
            </xsl:otherwise>
          </xsl:choose>
          <xsl:if test="$numSeconds > 0">
            <span>, </span>
          </xsl:if>
        </xsl:if>
        <xsl:if test="$numSeconds > 0">
            <span id="seconds"><xsl:value-of select="$numSeconds"/></span>
          <xsl:choose>
            <xsl:when test="numSeconds = 1">
              <span id="timeSeconds"> Second</span>
            </xsl:when>
            <xsl:otherwise>
              <span id="timeSeconds"> Seconds</span>
            </xsl:otherwise>
          </xsl:choose>
        </xsl:if><br/>
      </p>

      <hr/>

      <h3>Test Procedures</h3>
      <table>
        <tr>
          <th id="stepNumber">Step</th>
          <th id="action">Action</th>
          <th id="expectedResult">Expected Results</th>
          <th id="screenshot">Screenshot</th>
          <th id="actualResult">Actual Results</th>
        </tr>
        <xsl:for-each select="test/procedures/step">
          <tr>
            <td><xsl:number/></td>
            <td><xsl:value-of select="action"/></td>
            <td><xsl:value-of select="expectedResult"/></td>
            <td>
              <a>
                <xsl:attribute name="href">
                  <xsl:value-of select="screenshot"/>
                </xsl:attribute>
                <img width="80" height="60">
                  <xsl:attribute name="src">
                    <xsl:value-of select="screenshot"/>
                  </xsl:attribute>
                </img>
              </a>
            </td>
            <td></td>
          </tr>
        </xsl:for-each>
      </table>

      <p id="signature">
        Tested By: ________________________________<br/>
        Date of Execution: ________________________________
      </p>
    </body>
  </html>
</xsl:template>
</xsl:stylesheet>
