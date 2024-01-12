


How to setup/run/use locally:

# Get token to use in `download_activities.py`



1. install everything
2. Run `download_activities.py` with `python download_activities.py`
3. Get login/creds with `uvicorn authenticate:app --reload` (more just below)
3. run `$python extra_runs.py` // get polyline for each activity
4. run webserver with `flask run`

## 2024-01-12

I'm not embarrassed, but I'd be tempted to be, that I only recently got Postman API calls working consistently around strava's oauth flow.

POST https://www.strava.com/oauth/token?client_id=111&client_secret=2e68a222416b4fbf8&refresh_token=333&grant_type=refresh_token

That's it. Take the `refresh_token` from the initial token request, with `grant_type` `read, read_all`, or whatever. I've got the exact call below. 



## 2024-01-11

I keep doing bits and bobs of work on this, and being pleased with the results, but not really writing down any of the work, so here it is, best I can remember it.

I now have a functioning URL-parsing website. This works:

https://joshs-mobility-data-54dab943ebba.herokuapp.com/?zoom=15&latlng=18.785264,%2098.992305#

Look that the query perams:

`zoom=15 latong=18.785264, 2098.992305`. So that lets me quickly snag any view I want.

that took getting query params, passing them through to the rendered HTML as a variable (easier to do in Python/Flask than in Rails) and then... lets see, something like:

IF there is a latlong param set, load the map to that view initially...

... after all the other JS has happened, if there is a zoom param given, set the current zoom level to that.

I cleaned up/debugged some broken Polylines that was causing some issues/persistent browser console warnings/errors.

I futzed with a CSS rule to disable some other warning:

per https://github.com/Leaflet/Leaflet/issues/4686\#issuecomment-476738312

added colored start/end markers, the clusters are interesting to me. Would be cool to show directionality of the line. Color it from a spectrum, beginning to end? animate it to wiggle or glow in a pattern that gives it movement in a certain direction?

I've done a bunch of other cool css stuff. Peep the file for more.

### Today's big discovery: somewhere it IS possible to get photo lat/long in/out of strava

What I wanna do now, and am super excited about, is to maybe add photo overlays on the map. 

I would love love love to be able to add photos to activities, and have it fetchable via the API

What I wanna do is explore the API response, in something that feels like a Ruby script or Rails console session:

https://www.strava.com/activities/10381720567

I'd long ago given up hope that this was possible. I'd imagined the feature as a once-was, but maybe no longer available.

Here's the Strava user forum threads I found:

https://communityhub.strava.com/t5/strava-features-chat/photos-no-longer-display-on-map-possible-to-adjust-settings/m-p/1984#M438

(strava, I'm still having issues, and I think the photo URLs + latlng information IS NOT AVAILABLE VIA THE API!!!!!! I would gladly sign on as a contractor to finesse this feature into existance, and then wrap up my employment at Strava)

Here's what I can see in the web UI:

![webui](/images/2024-01-12-at-12.07-AM.png)

BTW, here's the photo I want to render to this map. Cool photo, huh?

https://dgtzuqphqg23d.cloudfront.net/QThlg8qH8Ci0kjAhbDXUOW0LAD1z_TTbvDs3lWNkM6Y-2048x1536.jpg

It's got two photos, from my DRONE, I wonder if it matters. The drone includes geolocation data, I thought I'd told my phont to include all available photo geolocation in the files....

So next, since I can confirm a RECENT activity, with attached photos, that are rendered to a map, I wanna do two things:

1. with a given URL, render my own photo/pin equivalent to the map (already almost done)
2. with a given activity, somehow find an attached photo? I'm going to re-explore via a Ruby REPL-type thing, the strava-ruby gem: https://github.com/dblock/strava-ruby-client

Next, here's what I've got for my pop-up now:

The blue one is clickable:

![clickable](/images/2024-01-12-at-12.11-AM.png)

This is what happens on click:

![drone photo visible](images/2024-01-12-at-12.12-AM.png)

I'd like it to open up into a full-screen photo on click, and i'm gonna see if I can make the marker load with the pop-up already opened...

OK, here's something that sorta works, I just added the final `openPopup()` call:

```javascript
 var photoMarker = L.marker([39.728373, -104.940488], {
      draggable: true,
      title: "i'm a title! This is where this photo was taken",
      style: "background-color:black;"
    }).addTo(map);
    photoMarker.bindPopup('<img src="https://dgtzuqphqg23d.cloudfront.net/QThlg8qH8Ci0kjAhbDXUOW0LAD1z_TTbvDs3lWNkM6Y-2048x1536.jpg" style="width:200px"><p>this photo came with geodata, as it was taken on a drone I was flying at the time.</p> onclick="this.requestFullscreen()"').openPopup();
```

gonna maybe write raw HTML that simply makes the image a clickable link, click to go straight to the img source?

```javascript
let images = document.querySelectorAll("img");
.leaflet-popup-content > img:nth-child(1)

addEventListener("click", (event) => {});

img.addEventListener("click", (alert('hi')) => {});

onclick="this.requestFullscreen()"

```

Good progress:

![js alert](images/2024-01-12at12.42AM.jpg)

I'm leaning into this being heavy iteration:

```javascript
let thumb = document.querySelectorAll(".leaflet-popup-content > img:nth-child(1)")[0];
thumb.addEventListener('click', function() {
  this.requestFullscreen();
});
```

copy-paste friendly. Used the `ctrl-opt-i` element selector to click the image, find it in the html, right click the line of html, `copy css selector`, used that in the `document.querySelectorAll` to get the right img. when I was `querySelectorAll('img')`, I got thousands of results. the map seems to use a lot of img tags.

Anyway, making progress. I think `requestFullscreen` isn't exactly the right method but close. Now that I have this easily copy-pastable, I can reload the page, clear the clobbering mess of event listeners I added all over that bit of the DOM...

`onclick="window.open(this.src, '_blank');"`, I think. 

Heck yeah, that works. 

- https://stackoverflow.com/questions/67815853/how-do-i-make-an-image-full-screen-on-click#comment135891074_74505101
- https://www.kirupa.com/html5/finding_elements_dom_using_querySelector.htm
- https://stackoverflow.com/questions/2226953/how-to-attach-onclick-event-for-a-javascript-generated-textbox
- https://www.w3schools.com/jsref/event_onclick.asp

Lets work this back into the application...

ok, partial success. A little issue getting the query selector just right. It's so janky on the front end, but it works.

I'm now going to take a break from the thumb nails and see if I can remember how to quickly access the strava API calls that'll let me inspect this activity blob. 

I think it'll be quick. I've got an oAuth key of some sort...

https://www.strava.com/api/v3/athlete/activities, with an authorization header of `Authorization: Bearer asdkljfaksldjf`

Returns a big JSON blob. Here's the first of I suspect 30:

```json
   {
        "resource_state": 2,
        "athlete": {
            "id": 38072598,
            "resource_state": 1
        },
        "name": "📸 12 pitches, mostly. And delicious food",
        "distance": 13523.5,
        "moving_time": 3389,
        "elapsed_time": 23729,
        "total_elevation_gain": 68.3,
        "type": "Velomobile",
        "sport_type": "Velomobile",
        "id": 10541779662,
        "start_date": "2024-01-12T00:11:31Z",
        "start_date_local": "2024-01-11T17:11:31Z",
        "timezone": "(GMT-07:00) America/Denver",
        "utc_offset": -25200.0,
        "location_city": null,
        "location_state": null,
        "location_country": null,
        "achievement_count": 0,
        "kudos_count": 0,
        "comment_count": 0,
        "athlete_count": 1,
        "photo_count": 0,
        "map": {
            "id": "a10541779662",
            "summary_polyline": "eloqFhxp_SFIB@?GCHAEA@DIEf@@L@I@HCPJUAIGFD@KTAEGF@C]A[BIDCV?`AJNd@LrBKrDC~FH~GCNBBFClNDbLFbB?rAGdTBvABNBt@CvLDfLAbCD`h@CdHD^X`BU\\ERGr@Ar@DzGAdEFjKGbC?dGG|EB~CCxC?HDEBDBl@@jGCzA@~C@xADDCzA?nIA\\MDElCDF?HEf@@vAb@jFExEF`DAvCHJBVErDFN@v@DThGIfI?NF^@rFGZ@JDDHF~CAjMBp@CzFCXIZLdAEpHCZIRwAbAg@ZUDy@GIFBBCEBABNCAGkAFAFTCDKADn@DE?g@@KB@MAAFEGDCH@EB@FEMCJG?BMGMNJDJB??EEDCABC?FEIFBGCAHAGDHBIEF?OICDBBNDG?D@EAFEMBJCBDG@FEK@FIDJA?G?J?Q?DECDJ?G?L?M?J?K?J?K?H?I?DGCFEA\\ABACANBNEAGOB[Pm@Df@F?DHKEKI?L?OAN@Q?N?KCFCADB@C?H?KEN@I@DDGCA?G?F?IED?FBA@I@DCA@A?N?QAT@UABACBH?K?T?U?P?K?H?IG@DB@I?P?OCFAI@FD?AB@IAF?I?T?KE?DCMs@BAC??BB@SSBAXr@ARFDGBAEDj@COHXAMb@H`@APMDQl@_@DG?GG@S`@QDW\\k@DOPWFw@MaADaHMkBFiDG_@GoGDYEIQIiCDwAEsB?kDCeAL_ANCZDJZ?d@ANE?@FSPBCADDFBAIIBC?IMLBDE@BICKH?BHPWBW?m@OO]@IOB[Cq@By@KwB?cFC{@@WDUEg@C}ADwJI}CB[Li@BcBBSFMTM~AwANY?MGEKeAy@wBOQc@IkBB}@LBF\\DPA?E_@IMB?JB@P@FGQ?AHFV@IEDD@A@g@U@KBEVK^JMDCMvBFDABKCgGDSEi@AcFAFGDFaDGaAB_@LQGyAFw@@kBCw@CiBByAGkCF_CAyBDyAGgB@_FGaBAiEBmAJc@Gw@BwDGwB@sGBwCGwHFk@EoEB[IeAFgDAGSEAuBB]VO@cCBQz@aARY\\w@Po@X{C?YQsAUs@s@eA{@k@Oe@Ci@BgDEaCDs@EaA@gCB}BGqCH}CASKMWCiBLsBC_AS{BkAkASoB?MOCKBuJD_ACqAA{BBc@C}ADkALcAFaEEeDFuAEaCDmBC{DSmA?}AD_AGECBDzBl@DPO@DAELBBWGBDWB?CKDFAKCFR\\O[",
            "resource_state": 2
        },
        "trainer": false,
        "commute": false,
        "manual": false,
        "private": false,
        "visibility": "everyone",
        "flagged": false,
        "gear_id": null,
        "start_latlng": [
            39.73330959677696,
            -104.94868962094188
        ],
        "end_latlng": [
            39.733289647847414,
            -104.94868266396224
        ],
        "average_speed": 3.99,
        "max_speed": 16.994,
        "average_watts": 123.8,
        "kilojoules": 419.6,
        "device_watts": false,
        "has_heartrate": false,
        "heartrate_opt_out": false,
        "display_hide_heartrate_option": false,
        "elev_high": 1644.6,
        "elev_low": 1594.0,
        "upload_id": 11279732714,
        "upload_id_str": "11279732714",
        "external_id": "d477746c-a108-40e8-9967-614a29203e0c-activity.fit",
        "from_accepted_tag": false,
        "pr_count": 0,
        "total_photo_count": 5,
        "has_kudoed": false
    },
```

The `total_photo_count` is distinctive to me. 

That's an activity from today, though. Lets jump to a specific one, I still have a tab open to https://www.strava.com/activities/10381720567

So, I made a guess, and in Postman did `GET https://www.strava.com/api/v3/activities/10381720567`, and sure enough:

```javascript
{
    "resource_state": 3,
    "athlete": {
        "id": 38072598,
        "resource_state": 1
    },
    "name": "Big day",
    "distance": 25504.1,
    "moving_time": 6095,
    "elapsed_time": 38981,
    "total_elevation_gain": 159.1,
    "type": "Velomobile",
    "sport_type": "Velomobile",
    "id": 10381720567,
    "start_date": "2023-12-14T13:20:42Z",
    "start_date_local": "2023-12-14T06:20:42Z",
    "timezone": "(GMT-07:00) America/Denver",
    "utc_offset": -25200.0,
    "location_city": null,
    "location_state": null,
    "location_country": null,
    "achievement_count": 0,
    "kudos_count": 0,
    "comment_count": 0,
    "athlete_count": 1,
    "photo_count": 0,
    "map": {
        "id": "a10381720567",
        "polyline": "eloqFtyp_SGB_ADCN?r@N~@B`@@tHAzA?~ERJtAKj@AjC?~@CnF?zAC~DBLHCNAtBFtL@nRCNB`BErBBhA?fIDrCA|GFjDAtJFrg@CbFFx[I`OBbMC~BBtFAbGAZ@tDCjCB`B?ZGFC\\@b@ZzCDz@CfEBbJAlL@jGCnBEhMHnF@vDD~AFX`FKfJCt@IZM\\EH?DDABE@BDE]B@@KDEB@@JCFC@GS?D@KCTBU?NAIBBAC@BACAB?C?J@CAC?F@UAN@@AKBJEGACBA@L?C?I?JAC?D?IAN@QANBCCWBLCHB@AB?U?LDJAAAKA@@OAR@OAHCIBD?AAN@S?F@AAC?D?GA|@?IC??@F?ICAGGHB@DE?D@ABBLI?@KDBFIAEEA?CK@@AD@A@BBC@FEAC@GIEB?CJADEJBDJIBGA?EEIED?CEDAAD@?A@@FGB@EBECLADBJ?HJ??ECAB@EABC?@@?EC@BAAADC?BC??BCCB@C?@B?C@??@CAA@?AC@?CBB?BD@A?@B?CBB?A?CCB?E?@?C@BAE@??B?GA@AECJCBDCBJ@AEE[IUT_@Bc@@aCCoLDSAGESCuFCk@@IAGCEEGi@D}BCmA@uBDcDB]?uAFa@FGL?LDBL?nAE`@EO?E@@@DIIDDC?D?@DEGB?A??@B?EAB?A@AA@BAAB??ABBEAB??CC?@FAAB@EADBAB?C@C@@ABEG@E?DAAC@@BCCB?BDAEHHDAKIBBAFE?GCDA?C@BAE?D?EBF@CBDCFFA?GIABC@GECE@@AFLAD@GABEEBB?BAEN?BBCDCCAF@CCCD?CAAE?@CA?DCCBG@DC@AC@@AFE@D?AC@FDC@@COD@BFABCGBCABE@?CCEF@?FECBA@BB?@DEDEE?FBBAEBDCK@DCBEMFSBHCJB?C@AG?HBAACA?@GCADACJE@BABEA@CCDDCCADBFAK@D?C@J?ODFA@CAA@BF@EBBAIA@CCEBCCDB?D?GCACI@@@JB@?GFLBE@@ECFGIA?BD?CFCEBJ?EDECGA@DD@ACJ?AE?AI@P?ABDAQBB?EAAADAGC@?E@F@CDHE?ACHBAACA?BHFA?ACA@?GCB@@DAAGCDEG?BD@?HCABGB@AA?FAIA@AKBX@AEMAB?J?OA@?CC?CFLF?A?BCEC?@A?D?IFD@ACEAGGIDT?CA?FC?AG@ALGAQODEJ?FB?BEC?FAK@B?ABDCC@B@EBA@DCABA?DECDB@GB?@DC@EG@FB@BABBKWF@@BGPEHAKBH@AGKABDACG@D@KAC@PDABG?BC@?BCIOABDJFBC?@CA@@BEE??DBBBCEA?@B@FHCCCFD?IQEH@B?CBE?BAC@JCGD@EEFF?C???@AA@DCB@@ACBEECABBABBEA@G?J@ACC?B@GCCAD@DEA?CB@@C?BF@@AC?CC@FGIDB?DCI@J@AEGD@@A@FEGABG?JA@@IMFFCCBFAEB?CDDDSNHKAEBE@BA@D?HBCI?sAEIEAY@GMAiCIGICkNJ{AAYC_BBcBCaCHaM@w@Do@TWNUPqAjBk@h@ULWFWBeBDe@HcA?aAEe@I[OYWKM?C@@I@Yy@WkAEIGEI?g@LoElBgBl@w@Tu@JcAD[A]EWKG?WNcC^]JKAcAb@qBrAo@l@k@v@kBrDaA~Au@t@[VgEtCq@j@YVq@x@{GbKq@~@y@t@}AfA{@r@oArAm@`Am@fAiA`DkCvGuBzG}AlGM\\_A`Dy@~Dw@zEsBnHw@bD}AnFe@tAg@fAC@@Om@fBu@hBcAtBa@|@m@hB[hAe@tBo@pBc@hAyBpEo@jBe@fBe@rBW|@S`@IXQFg@r@E\\Az@@zAE^GHAHN^BdBAbHDTHDXEb@?NDBD?JG|A@n@Cd@B`AEFICEBRAC|@BfAAj@E@_AAQGIIFkABgBCESFINAJANB?NQHJGCADDGLJF?A?AFBZCd@J\\BXFBJG?@GF?@FBA@MOKCEEH?BJKWCCE@DH@ABmBDADH?DC@?ECC?BDHCVD`@?`@FRJGBKCCC@ABDJ@ECGGAG@SV?DB@CF?P@HFFBCIGBk@BAVEBGEIGDDFADI?@IGH@?A?F??GIBBDCE@?@DJBI@ACRFGL?FBFDBFCAGB@@ACIMSAWBCDR?CIDG?A@B?E@@E@@CC@F?C?@BAAACDDGGDB@G?FAAAB@CCABB@AEA?@BCCDAE?DDIGDHAE@AEEF@CAABBBCG@DBAABEGFDA@CGBA?DA?@@ACB?E@CEF?I?DDD?MGJBE@DH?CC@D?BAEA?DACBB@?A@?G@?EB@AAC@H?C?@D?E@AC@C?HAEBACFF?C@BBRB@B?CAA@ACGICG@ECJBGABBA?@AE@AC?BA?BCC@F@IAD@?E?D@A?A?@C??@?AD?CA@@C?DCCBCABB?CCB@CBBAA@@DEG@F?JDUEAE@DD@CAEGDJCG@D?GABFBAB?CC?F@E?@?CAB?AB?A@?CA@BAC@@B?AA?BTFBFCEAG?DEE?CECE@?BCA@CC@D@I?@?ACBBAAB?CABDEEB?ADBACC@?C?BC@H@EADAC@AA@?B?E?D?CBCCDBCAB@@C?DACA?B@CCCLHCAFACABESFREAA@GEFKDPEM?@BC?LCMB@@ACBBE?@C?BFA?@DEQD@AA@@@@GEDHAEBAAPEQFNGODNGSJL?IGBBGCDBA@i@HVCC?FM@QJIG@YCEGCU@g@AYE?LE@F?GD@@CGF@CEBBB?GA?ERDI?@B?A@?CA?B@?GG@A@BBB?@EB@BBCHAKBAA??@F?MA?CBAAF@CFAC@CEGLG@ECCO@IJQRE@Q@mBE_AA{ADuACcFDu@@gEBq@H_@|@}AZu@Vu@z@kDd@qAx@cB^gA^u@HG?GDBBGp@gBd@oAfAoEh@aBlAgCb@s@RKV?DGHiAHc@vAcEv@oCvBgIhCoKHOPExEIN@LFLJFPDl@CzBBzBC^Ff@EbAGrCC^EFI@K?_CMoAAGECWJ{EA_EEu@BaA?CEEAG@?@EAJCBBCI?JHCIBk@DMPQ@GEG[?CCCGAMHc@|@wCT{@F[?DHSbA_EzBiIn@mBb@cAdC_Hv@gBd@}@h@{@n@s@r@m@dCiBVUl@o@hEoGRc@LQFEFABFhAmBd@o@f@i@lAcAhAw@@@BALMfBqAxEwEx@s@tBaBfAo@r@W`BWxCEvBOZErA_@vAe@nBu@rCqAzCaBRIL?E?r@g@tBsAp@g@xBiBHKLWH{AACE??OCCC@BUGeF?qBCaJLqLCaC@g@Jc@P_@tAoBNi@Dg@Cg@Sa@aBsBMa@Io@BE?DBA?B@OByGC}CBuIEwF@eG@gB?iF@eAAi@@EBAAeCBmAG{C@{IBkE?CCAAG?yCD_SAsHDkA@aDCoCBgGCyNB{A@OFINILANB~A?tCJd@ErDBzBCL?FDFC@KEwAAwAB_@HYDAX@vE?j@AF@DABGAm@GkAD_@?FHB?CCCD@?C?}@HCNFBPE\\?J@EAC?FF?C@AA@@?EAA?B@EC@@?A@@C?BDCE??BAG@F?AIIHD?CN?@AOAMHHB?B@G?@CA@@A?B??@?C?BAA@@?C?@?C?D?C?B?CA@@??A?@?QCUKECDDL?PBH?LCF@@CA@CG?A@BCE??ECDCEB@G@?C?BGGF}A@kCCk@@_@CMEIW@G?CGGcEBq@?aECi@B_AAuAD{@Cg@CiB@WR{@Bq@@cBBu@CkABgCCgAB{FA@@?EeB?g@Gg@?IBEGS@[DIf@@LCFGD?AED@?AE?HGDHC@CC?I?FCaACX?C@C?JG?BA",
        "resource_state": 3,
        "summary_polyline": "eloqFtyp_SgAHCN?r@R`B?pRRJ`CMvOGlELEdCHvc@ErBNn^HfwAI`O@|n@K`Ab@zF?df@IxPPfOFXhQOnB]NDCJE]JODLKFAWCTBUAP?OBJGKDJCD@QAK?V@ODXC[CVBMAC?x@EGF@KKGH^EMFBFQGCKHLWE\\GDJIBMQMDRC@AZNKAIEJLBAEQGNDCBJ_@QUTcADqP@cJSMo@BaIHwGLg@^JCvBKWBBDAALAOGDTFKI@JMCDGLNCUECE@DNPAIHAOG@BGINL@COHHAGGDCI@DJFK@DHIIDYBTEE?HBQILFGEDDH?ODF@FQKAINT?GFGIA@P?SFDCJGKDT@SIGNTIEF?KI@LFEGMDVEMAN?OIDLHEKHBMWDTDGILYQXAEFAKP?G?LJKWF@ETGH?KBHGIBS@PHICHSKNLDGED@?JJGBCQEHDECB?CFBAJAQ?JCMALJEMEJHQCL?IMJPSNJWNHC}AKKa@KAiCSKal@V}Av@qAjBk@h@m@TcDReCEaAYe@i@GBq@eCWOwK~DyBPyASWNmDh@uDvB{AdBmDrGqAlAsGxE_K|NsEpDoArA{AhCuExLuBzG}AlGmA~DqBzKiGbUqA~C@OiEdK_DzK}CzGo@jBcBxG]z@y@z@EtDOr@N^BdBAbHNZ|@ENDBPG|A@vCUFRAApDeA?[QJsDW@KZANRQHJI@ZBChANv@RCGHDF_@YLFUUHD?gBFEDHG@FdBHRLSI@DJAMO?SVFp@DAIGBk@^OEIGDBLO?F?ICVNGTHJJKQ]@[DRSDBGKF@EDAIADHEMF@ICF?KAJBDFGCFPTFCOY?F?IAH?G@BCRDOCIIB@@JZNQUOBB@DAFBBKSFRE?IQLPEUDREQFJGOHL?MGDBk@JVCD_@JIg@IA}@GYVGIBERHGGEJ@?L?MF@K?HEGCONISL[RE@QCcQF}FLqAxAsCxBsHxBaFdA{BvCaKpB{Dp@SRmBnCsIhGgVlFO\\HT\\@dIFf@QvF[HwEUBkPCWAJI?JH?u@Xg@e@KEUnHkXxEqM|AeDxAoBxDwCdAeA|EsHTWJDhAmBlAyArG{ExEwEnDuCzBgA`BWlH[zG{BnHsD`@IE?zEcDxBiBVc@H{AOUGoUJ{Q\\cAtAoBTqACg@Sa@aBsBWqAF@@OByGEkVBgUDG@sEG{CDgPEgDJocAHY\\KpRNHOGoDLy@jH?HIIyBD_@HJCGDA?}@XBAz@?IBHCGFAOGZ?]FHDBCAQCUKEBfAa@QF}A?wEIWc@EGaNFqEGqCTsAHkE?uOEmCKkAFe@t@ATUDHGCCaAEZ"
    },
    "trainer": false,
    "commute": false,
    "manual": false,
    "private": false,
    "visibility": "everyone",
    "flagged": false,
    "gear_id": null,
    "start_latlng": [
        39.73331638611853,
        -104.94890989735723
    ],
    "end_latlng": [
        39.73330657929182,
        -104.94868727400899
    ],
    "average_speed": 4.184,
    "max_speed": 20.634,
    "average_watts": 217.9,
    "kilojoules": 1327.8,
    "device_watts": false,
    "has_heartrate": false,
    "heartrate_opt_out": false,
    "display_hide_heartrate_option": false,
    "elev_high": 1644.4,
    "elev_low": 1581.9,
    "upload_id": 11112868960,
    "upload_id_str": "11112868960",
    "external_id": "304de00e-bcce-40ea-bc1d-94f4c6e8ec38-activity.fit",
    "from_accepted_tag": false,
    "pr_count": 0,
    "total_photo_count": 3,
    "has_kudoed": false,
    "description": null,
    "calories": 1480.5,
    "perceived_exertion": null,
    "prefer_perceived_exertion": false,
    "segment_efforts": [],
    "splits_metric": [
        {
            "distance": 1004.3,
            "elapsed_time": 165,
            "elevation_difference": 7.2,
            "moving_time": 130,
         
    "laps": [
        {
            "id": 35754386179,
            "resource_state": 2,
            "name": "Lap 1",
            "activity": {
                "id": 10381720567,
                "visibility": "everyone",
                "resource_state": 1
            },
            "athlete": {
                "id": 38072598,
                "resource_state": 1
            },
            "elapsed_time": 38981,
            "moving_time": 38981,
            "start_date": "2023-12-14T13:20:42Z",
            "start_date_local": "2023-12-14T06:20:42Z",
            "distance": 25504.1,
            "average_speed": 0.65,
            "max_speed": 20.634,
            "lap_index": 1,
            "split": 1,
            "start_index": 0,
            "end_index": 32783,
            "total_elevation_gain": 159.1,
            "device_watts": false,
            "average_watts": 217.9
        }
    ],
    "photos": {
        "primary": {
            "unique_id": "45ef90b2-5b41-4a1c-9c47-c0f4ed7bc6ff",
            "urls": {
                "600": "https://dgtzuqphqg23d.cloudfront.net/QThlg8qH8Ci0kjAhbDXUOW0LAD1z_TTbvDs3lWNkM6Y-768x576.jpg",
                "100": "https://dgtzuqphqg23d.cloudfront.net/QThlg8qH8Ci0kjAhbDXUOW0LAD1z_TTbvDs3lWNkM6Y-128x96.jpg"
            },
            "source": 1,
            "media_type": 1
        },
        "use_primary_photo": true,
        "count": 3
    },
    "stats_visibility": [
        {
            "type": "heart_rate",
            "visibility": "everyone"
        },
        {
            "type": "pace",
            "visibility": "everyone"
        },
        {
            "type": "power",
            "visibility": "everyone"
        },
        {
            "type": "speed",
            "visibility": "everyone"
        },
        {
            "type": "calories",
            "visibility": "everyone"
        }
    ],
    "hide_from_home": false,
    "device_name": "Strava Android App",
    "embed_token": "34e7fe2fd3ab1486f8da60c9c67c547e835111f0",
    "available_zones": [
        "power"
    ]
}
```

Huge blob. Most can be ignored, there's a few mentions of photos:

```javascript
    ...
    "photo_count": 0,
    ...
    "total_photo_count": 3,


    "photos": {
        "primary": {
            "unique_id": "45ef90b2-5b41-4a1c-9c47-c0f4ed7bc6ff",
            "urls": {
                "600": "https://dgtzuqphqg23d.cloudfront.net/QThlg8qH8Ci0kjAhbDXUOW0LAD1z_TTbvDs3lWNkM6Y-768x576.jpg",
                "100": "https://dgtzuqphqg23d.cloudfront.net/QThlg8qH8Ci0kjAhbDXUOW0LAD1z_TTbvDs3lWNkM6Y-128x96.jpg"
            },
            "source": 1,
            "media_type": 1
        },
        "use_primary_photo": true,
        "count": 3
```
ugh so annoying. Not sure how to get the photo URLs. I could maybe write a little scraper?

Every time there's a `total_photo_count` of >0, run a headless browser to the activity show page, use a `querySelectorAll` to get the image 

https://dgtzuqphqg23d.cloudfront.net/Vkf0NB3I6peD-pCt-iAfd234zHx2TVhYpZCSfI22_3c-2048x1536.jpg

Hm:

```javascript

let take2 = document.querySelectorAll('html.logged-in.clean.offset.feed3p0.old-login.js.no-touch.history.draganddrop.localstorage.svg.fullscreen body.logged-in.clean.offset.feed3p0.old-login div.view div.page.container div#view section#ride-overview.pinnable-view.with-border div#map-canvas.leaflet-container.leaflet-touch.leaflet-retina.leaflet-fade-anim.leaflet-grab.leaflet-touch-drag div.leaflet-pane.leaflet-map-pane div.leaflet-pane.leaflet-marker-pane div.leaflet-marker-icon.leaflet-zoom-animated.leaflet-interactive div.photo-marker img')
```

That works. Each element contains a nice URL:

`https://image.mux.com/AZV02huXXwvoi7kQSgHABN6JsucW54K8LZqd85rOj65Q/thumbnail.jpg?width=1012&height=1800&fit_mode=preserve&time=0`

Unfortunately, that object doesn't have any latlong coordinates in it. So, I could theoretically scrape the image URLs from Strava via automated headless browser, but that still wouldn't tell me where to place them. hm.

Googling "how to view geodata for photo"


## 2024-01-03

If you're forgetful, and don't remember why the strava code is returning `invalid`:

https://www.markhneedham.com/blog/2020/12/15/strava-authorization-error-missing-read-permission/

## 2022-02-28

I'm basically building https://metroview.strava.com/map/demo for myself! 

## 2021-12-05

## Getting creds for `extra_runs.py`

run `uvicorn authenticate:app --reload`

Visit localhost:5000, take that code, and use it in a `POST` to `/oauth/token`, with `client_id`, `client_secret`, and `code`

Here's what to do:

### Get `code` param

1. In a BROWSER (not Postman, because you need to follow the redirects...) go to:
2. https://www.strava.com/oauth/authorize?client_id=63764&response_type=code&redirect_uri=http://localhost/exchange_token&approval_prompt=force&scope=activity:read_all
3. approve it (I have a google account, am signed into Strava, etc)
4. grab the `code` param from the redirect after approving

### Use `code` to get `access_token`

do a POST to Strava via Postman to get the access code:

```curl
POST https://www.strava.com/oauth/token?client_id=63764&client_secret=2e6c5168e3b97a9c0975e5377041b8a416b4fbf8&code=0a0f72c337dce3ad0f4efd2ff86928fdd471fff3&grant_type=authorization_code
```

### Use returned `access_token` in `extra_runs.py`

replace the variable, do `python extra_runs.py`

It's working! Huzzah for polylines. I've got a TON more data in Strava now, so this will be a cool map rendering.

https://www.markhneedham.com/blog/2020/12/15/strava-authorization-error-missing-read-permission/

# Goal

To render my nephew's currently-being-tracked bike route (via my GPS watch and my bike) on an OSM map layer so he can pan/drag/zoom/explore in a way very similar to google maps. 

## Most current goal:

Get all of my Strava run polylines, render them to a map.

### Get what little I currently have visible on Heroku

I want to duplicate the functionality visible in [https://www.markhneedham.com/blog/2017/04/29/leaflet-strava-polylines-osm/](https://www.markhneedham.com/blog/2017/04/29/leaflet-strava-polylines-osm/).

I'd like to know how to deploy it to Heroku, so it's publicly visible. I've deployed Rails apps before, not Flask/Python apps. (here's the working version on Heroku: https://josh-strava-heatmap.herokuapp.com/)

It's working locally, but not on Heroko:

![what to do](/images/2021-05-23-at-11.04-PM.jpg)

### Translate the Python over to Ruby

```python
# app.py
from flask import Flask
from flask import render_template
import csv
import json

app = Flask(__name__)

@app.route('/')
def my_runs():
    runs = []
    with open("runs.csv", "r") as runs_file:
        reader = csv.DictReader(runs_file)

        for row in reader:
            runs.append(row["polyline"])

    return render_template("leaflet.html", runs = json.dumps(runs))

if __name__ == "__main__":
    app.run(port = 5001)
```

I need to bring this over to Sinatra and Ruby. Seems... doable, though not straight forward.

How about:

```ruby
# app.rb
require 'sinatra'

get '/' do
  @runs = []
  erb :index, locals: { runs: @runs }
end
```

Ended up with:

```ruby
get '/' do
  @runs = []
  File.read('index.html')
end
```

OK, now I need to get runs....

# Starting from scratch, Early April:


OK, copied-and-pasted. It's been a while since I've written Python, and I've never actually made a Flask app, so I'm hoping it all runs without some hidden, subtle dependency problem that's really obvious to experts but not me.

here's how this sounds in Ruby:

> Oh, you tried to `ruby file.rb` and got an obscure error? I know that means your $PATH is wrong, RVM. 

Ugh. 

I guess I need `pip`, installed.



I need an  API key from Strava.

[https://www.strava.com/settings/api](https://www.strava.com/settings/api)

Got it. I'll need to save it to my ENV to avoid accidentally committing it to Github:

```
> export STRAVA_TOKEN="12398q798798798uyfhjsdkan"
> echo $STRAVA_TOKEN
```

OK, update the value in `extra_runs.py`, getting close to being able to run it.

Now I'm getting:

```
> python extra_runs.py
Traceback (most recent call last):
  File "/Users/joshthompson/me/strava_run_polylines_osm/extra_runs.py", line 22, in <module>
    r = requests.get("https://www.strava.com/api/v3/activities/{0}?include_all_efforts=true".format(activity["id"]), headers = headers)
TypeError: string indices must be integers
```

Something's breaking in line 22. I bet there's an authorization error somewhere that's causing a bad datatype in the response, so the function is breaking as it tries to execute on an error message instead of a blob of JSON or whatever.

If it were ruby I'd stick a pry in it, but it's pry so I'm googling `pry breakpoint`. 

Turns out it's `breakpoint()`

add it right before the error, and:

```
> python extra_runs.py
> /Users/joshthompson/me/strava_run_polylines_osm/extra_runs.py(23)<module>()
-> r = requests.get("https://www.strava.com/api/v3/activities/{0}?include_all_efforts=true".format(activity["id"]), headers = headers)
(Pdb) activity
'message'
(Pdb) response
{'message': 'Authorization Error', 'errors': [{'resource': 'AccessToken', 'field': 'activity:read_permission', 'code': 'missing'}]}
(Pdb)
```

Ahh, reading the blog post more clearly, I can see part of what he's getting at. I copied-pasted a different (earlier) document in, I can see what he's working on.

## Strava API Basics

OK, I've never interacted w/the Strava API before. I was hoping it was as easy as getting a private key from Strava, saving it as an environment variable, and running the script, so I tried all that.

No dice. Getting a 401 from the strava API. I don't know python, and don't yet _fully_ understand API calls well enough to know just by reading this python code, I can debug it in Python, so I'm going to rebuild the request in Postman.

In postman, I'm going to try a simple `get` for:

```
https://www.strava.com/api/v3/athlete/activities
```

Ah, Authorization problems. Here's the response: 

```javascript
{
    "message": "Authorization Error",
    "errors": [
        {
            "resource": "Athlete",
            "field": "access_token",
            "code": "invalid"
        }
    ]
}
```

It's expecting me to authorize even what seems like it should be "public" data. Surely some of the Strava API is public to hit w/o authorization? Oh well.

I've been lucky enough to have some passing familiarity with what's going on here, because of some painful past experiences. 

Let's get authorized w/the Strava API.

I think we need to create an app w/in Strava.

I googled things like `authorize strava api` and `how to generate strava api key` and found a few sorta haphazard guides. It's still not screamingly clear what to do here. Maybe it is to you?

- [https://developers.strava.com/docs/authentication/](https://developers.strava.com/docs/authentication/)
- [https://yizeng.me/2017/01/11/get-a-strava-api-access-token-with-write-permission/](https://yizeng.me/2017/01/11/get-a-strava-api-access-token-with-write-permission/)
- [https://developers.strava.com/](https://developers.strava.com/)
- [https://developers.strava.com/playground/](https://developers.strava.com/playground/)

It seems like I need API keys, so I created an app, and tried making the public and private keys. Meh, I need to go get an access token from the Strava oAuth server (I suppose?)

Reading through https://yizeng.me/2017/01/11/get-a-strava-api-access-token-with-write-permission/

----------

## POSTing to strava.com/oauth/token

OK, here was my second API call attempt:

![strava 2nd call](/images/2021-03-28-at-2.11-PM-strava-api-2nd-call.jpg)

Third attempt, more closely reading the yizeng.me piece:



## Strava API 

---------------

Two weeks have elapsed since I wrote the above...

Onward. 

I need to authenticate against Strava. No idea how to do it in Python, so I'm firing up Postman and seeing if I can recreate this series of calls there.

Working through [this guide](https://developers.strava.com/docs/getting-started/#oauth)

### Step 1: `Go to https://www.strava.com/settings/api and copy your Client ID`

Easy. Mine is: `63764`

### Step 2: `Paste your Client ID into this URL: http://www.strava.com/oauth/authorize?client_id=[REPLACE_WITH_YOUR_CLIENT_ID]&response_type=code&redirect_uri=http://localhost/exchange_token&approval_prompt=force&scope=read`

OK, slightly reformatted:

Go to: [http://www.strava.com/oauth/authorize](http://www.strava.com/oauth/authorize) and include the following query params:

```
client_id=[REPLACE_WITH_YOUR_CLIENT_ID]
response_type=code
redirect_uri=http://localhost/exchange_token
approval_prompt=force
scope=read
```

This is... extremely not intuitive. Let's do it in Postman anyway:

Sigh, didn't work in postman, may have made a typo.

Sure enough, when I visit in the browser:

[https://www.strava.com/oauth/authorize?client_id=63764&response_type=code&redirect_uri=http://localhost/exchange_token&approval_prompt=force&scope=read](https://www.strava.com/oauth/authorize?client_id=63764&response_type=code&redirect_uri=http://localhost/exchange_token&approval_prompt=force&scope=read)

I get what's expected. 

### Step 5 or 6: `Make a cURL request to exchange the authorization code and scope for a refresh token, access token, and access token expiration date (step 7a from the graph). Replace the client_secret and code. `

They include a suggestion to use Postman, and I did. Success:

![success](/images/2021-04-04-at-11.41-PM-talked-to-strava.jpg)





This is unreal.

Next, to use Swagger, have to auth their app to this odd "strava app" i have, so I got to `https://www.strava.com/settings/api` and set the `authorized callback domain` value to developers.strava.com

### Step 8: Pick rightly (but you have to figure it out) the scopes to authorize the swagger API

I wanted it to have all read access, so I checked too many boxes. Turns out you keep getting errors from the API if you have anything but the first box checked.

The errors are cryptic, took me 4 attempts. 


![ugg](/images/2021-04-04-at-11.49-PM-bad-request.jpg)

### Step 11: Find a taste of success with Swagger

Check it out! 

I finally authorized Swagger to my account, and:

![it works](images/Screenshot_2021-04-04-Swagger-UI.jpg)

I can see my athlete stats! I'm going to retry this python script now...

Feels like we might be getting close to it working.

Damnit. `response` still throws an authorization error.

I'll work towards the API call from this script in swagger

Here's the relevant code, to recap:

```python
token = os.environ["STRAVA_TOKEN"]
headers = {'Authorization': "Bearer {0}".format(token)}

with open("runs.csv", "w") as runs_file:
    writer = csv.writer(runs_file, delimiter=",")
    writer.writerow(["id", "polyline"])

    page = 1
    while True:
        r = requests.get("https://www.strava.com/api/v3/athlete/activities?page={0}".format(page), headers = headers)
        response = r.json()
```


AAAAAGH THIS IS SO NON-INTUITIVE!!!

I re-ran the script, but got the same error as before:

> {'message': 'Authorization Error', 'errors': [{'resource': 'AccessToken', 'field': 'activity:read_permission', 'code': 'missing'}]}

Not super helpful.

I tried re-exporting my `STRAVA_TOKEN` environment variable to different values gathered from `https://www.strava.com/settings/api`, but no dice.

Then remembered that I got this access token in the Postman `POST` request to `https://www.strava.com/oauth/token`

So, opened that up, checked the output, thought "yeah, lets try that":

![nailed it](/images/2021-04-05-at-12.01-AM-finding-the-right-environment-variable.jpg)

This has been _shockingly_ difficult.

Anyway, how do I know this is the right value?

simply because I got a different error message. Behold, the obvious difference!

![isn't it obvious? an inscrutable Strava API response](/images/2021-04-05-at-12.03-AM-self-documenting.jpg)

so, lets fix this. I'm going to rebuild it in Postman first.

![got it](/images/2021-04-05-at-12.06-AM-activity_read_permission_missing.jpg)

Finally, it seems like the response tells us the problem. The `api` seems to want a parameter/key-value pair submitted 

### Step 27, reauthorize Strava app, update `scope`, get "privileged" token:

[https://www.strava.com/oauth/authorize?client_id=63764&response_type=code&redirect_uri=http://localhost/exchange_token&approval_prompt=force&scope=read_all](https://www.strava.com/oauth/authorize?client_id=63764&response_type=code&redirect_uri=http://localhost/exchange_token&approval_prompt=force&scope=read_all)

See that last query param, `scope=read_all`? I'm trying that. It was `read` before.

Big difference. ¯\\\_(ツ)_/¯ 

Ugh. No dice.

## Step 56, pull your hair out, pivot

Reading [https://markhneedham.com/blog/2020/12/20/strava-export-all-activities-json/](https://markhneedham.com/blog/2020/12/20/strava-export-all-activities-json/)

Maybe I can make this work, and learn the minimum Strava API stuff I need for the rest.

```
pip install stravalib fastapi uvicorn jsonlines
export CLIENT_ID="63764"
export CLIENT_SECRET="client_secret"
```

Copy/paste what he recommends into `authenticate.py` and per his instructions, in my terminal I run:

```
uvicorn authenticate:app --reload
```

And we've got a web server running.

Feels like the Sinatra of Python.

Following his instructions, note that you'll have to `mkdir data && touch data/activites-all.json` for the script to run.

Kept running into errors, realized the file open mode wasn't `open or create` it was just `open`. 

Great success! I've got data!

back to `extra_runs.py` - I bet I can just read in the JSON file I just created...

## References

- [Leaflet: Mapping Strava runs/polylines on Open Street Map](https://markhneedham.com/blog/2017/04/29/leaflet-strava-polylines-osm/)
- [Above author's gist w/the code (python, flask, leaflet)](https://gist.github.com/mneedham/34b923beb7fd72f8fe6ee433c2b27d73)
- [module not found error](https://stackoverflow.com/questions/44913898/modulenotfounderror-no-module-named-requests)
- [https://www.reddit.com/r/learnpython/comments/g135yz/strava_api_code_missing/](https://www.reddit.com/r/learnpython/comments/g135yz/strava_api_code_missing/)


## TILs

```p
> python extra_runs.py
# ugh, missing module. how do you install modules in python?
# what's python's version of RBENV. Pip. OK. Oh, I have pip, guess
# I don't know how to use it.
> python -m pip --version
> pip install requests
$ python -m pip install requests

environment til
```

- how to run basic python app on heroku?

```
pip install gunicorn
pip freeze > requirements.txt
```

https://medium.com/the-andela-way/deploying-a-python-flask-app-to-heroku-41250bda27d0


```
https://devcenter.heroku.com/articles/buildpacks
```
https://dashboard.heroku.com/apps/b0a05afc-05aa-4d23-973b-0d664a39ecfc/activity/builds/1e866a44-9dcc-4825-a016-8d0f715b286b
https://devcenter.heroku.com/articles/buildpacks#setting-a-buildpack-on-an-application

