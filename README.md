# Esther Congestion Control

A SSCCA (super Simple Congenstion Control Algorithm).

## Overview
Esther Congestion Control (ECC) works as a closed system negative feedback loop.  

A sender periodically send packets containing a timestamp and the period at which it sends.
  
A receiver listens for those packets, and measures the time between received packets and compares it to the expected period.
  
If the measured received time is equal to the time given in the Sender's packet, the Receiver will request a speed up, up to a pre-defined limit.
   
If the time is greater than period defined in Sender's packet, the Receiver will send a "slow down" message.  

## Sender
ECC Senders periodically broadcast packets over a network. It also listens for replies from receivers indicate a "speed up" or "slow down" message.
 
The rate at which the Sender transmits these packets is adjusted according to responses from Receivers.

## Receiver
Receivers listen for ECC packets, and, of needed, replies with a speed up or slow down message.