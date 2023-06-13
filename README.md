# The open-source Sequential Compression Device

## Description
The enhancement of an OS Sequential Compression Device (SCD), which combines software and hardware components, to create a suitable hospital device involves a meticulous and iterative process. The objective is to optimize its functionality, usability, and effectiveness, ensuring it meets the specific needs of healthcare professionals and patients alike.

This project has been initied by Schara et al. from Rice University, Huston, and was taken up for a master thesis at UCLouvain by Arthur Van Geersdaele and Thalie Sarafidis. 

## Structure of the .git
A directory has been created for every aspect of the prototype:
- The eletronic design
- The Arduino SCT Software
- The pneumatic band conception
- The risk management (empty at the time this txt file is written)

Don't hesitate to create a new branch for every new iteration of the prototype.

## Support
Arthur Van Geersdaele permanent email: arthurvg@gmail.com

## Acknowledgment
First and foremost, we would like to thank our supervisors, David Bol and Benoît Herman,
for their guidance and support during this academic year. Without their assistance and
suggestions this work would not have been the same. Thank you for all the feed-backs,
your ideas and critiques always helped us to progress.

This thesis could not have existed without the financing by the donations made during
a fundraiser launched by the Louvain Foundation in the first months of the Covid-19
pandemic for the development and distribution of open-source medical devices. We want
to thank the Louvain Fondation and its generous donors. Their donations allowed us to
work on a exciting project with meaning in our eyes. We hope they will be proud of the
work we accomplished.

Any opinions, findings, and conclusions or recommendations expressed in this material are those of the author(s) and do not necessarily reflect the views of the Louvain Fundation.

## License
This project is published under a Creative Commons CC-BY licence by Mark Schara, Mingde Zeng, Jumet and Daniel J. Preston in 2022.

## Overview

<img src="https://lh3.googleusercontent.com/uw4Hd-o32ru7BUOAbB3s1_LTyGWp65Da7H4i2JahnDTs6Ar5mRC0plo9FD7Agp0bvpjEJgBAzZyAgz1ODGIi2wvJs8SYI_CQhsvGnffs6thqfykDg9P1XCusFHrppcjr6rPDV2xLFMm2J6h1_0szi65yBpU9lWnKJ5rSwq3ubrPiXOT_1Hac90khSHL-h9MIdfPEApXJ7mb49-ZajqbDAtYwvUaOlETLIzgfOJBsA7sgyJlOT0yt2YbMv3GpUzhQ7PZIO09rDewyO8hCpPbQGOBm8Ick_VoB60gErlMK2dXj0LoxxpactQIRyAUKXMT05njngqidN9JbIh-tRAUxA39pvNOagiIaNs5qxKZ-geMXMUUh1KSzz2DNqUnsM8orgHhYX2Z4jMH79dZ6N7b7EV5a0ui3jc0EpDjqQzk9BoFseqaJtgzpXc6yy1WcyEozbitjDjpmVjW0ZTTrs3AYGii3fPwaPT2IzfByc1A8-G45BEoATe_FdRTkSiPQbXl_wRTKA6jdFILU7RyWDa_GA-kC7WXoMVRxeJdeWwyOOHT0UmKAZJIgE65j3RBG2r4TC7Gl7iSvzkSNGHxynlwCkUSfovuU3pucTX-aKGDkqSQwL4wkBvoB6Ym8yYRcVpI8htvWQc-uD0VXunMLr2rw7ekdo4kNAkBoA2MiCF9gJd0XxWyFrzWacRQjk8esgcvGre-oOjwujPdAQZGW7fqC3aWRuqOh0DKvhIdmAMbS7yQGlrnzOG0Ggk1G-W8OMzjK_TbKKGWceZHYmYRxAKX5-ZmQkzlQtpemMCyEXQ6HRnF8I7hZkuqrldg572jk0Rx_gl7yNCIeYkAO3rlNBZZVjHIyX9b472KIMveLa0yus4CzzZgd-NwYGYQfPhTc1JryEc0u7FGAJacYXIKgzX_jPv6EOYvD4NDPg4XLLxr0yGj_X_Otbf04HedCNWvO0OjOTbKVjZOo1jsq=w733-h977-s-no?authuser=0" alt="Image of the OS-SCD device interface" width="400"/>

<img src="https://lh3.googleusercontent.com/Dr_NfxmwPY0K1YTv_ehdX9OtSePjZ78id5i1sB04MkSCgEVkiPq_8iiFihfI5J00OjZHkZ0deeg7UaLteDr7LWMCece_ab0Vw5Il7_U0E2uyAFjOePnH3NXgfk2ZkVE7RpeCpILe7u4ZPhRlrQjADNLQK_58WDQn5HkZlI4wLSBhz05n7m1EOXfhF8xy8OvQAWsfo6RyBnK645H2nGPrk9d-_yMhf9HEUxVTjDkGdHXVTFZBLDnnyHQe9D7KOGfo5nrVeuhQoxbiN9QcBuIFzbtIWOAwTFWqvj5J3GjWftTaJEh-m1Oy7EkQvkPj9ex42rP_osEGtsQqNNyMr3QaofZXj-Uy6eVulfEoNjEmSsVgtUkAfHTFT5AhrzDPHvB2be8uBCjqXweLyB7Fhbobb_xbGfHqEjwkdHPvFzOBjJANuh43Aq9wYq77yR5ow3oTm-2vxnBpsaj6Ve8TEJazd0Bu5pSeH6s7i7d1IfVqitgE51EH6LeigY5GAUvsuZOBZ0eehkLnl8iy1QfrEJfJVwv9WL8W_5lmgF8XCZBhuTt4Z2aaOZbYOsfVOtdC1uYcmMr5mpoLeeDPwn6HvT3Pd-_AOCjC7dbROUaku0U2HrVSjMNkcciU3a-Hpw60i7aEXLDpbTqlfjllnTDz_P1NWJCVKSfnPY1kHBLqVN9ml2ZvrCgm_1u2Otnn8RhmmaHpN97wW-rxY3Qdlch1aUyDjVVmWPLI5jj9wrfD_LrI_JSu00dxK9zb0eq971x0ClWP4Ui6oKMWjEa43AaMuNEn7Y8gxKlC3ilPhgGlOSuHAD3CaqQqL1tIt0N39mfXXprw-5bhIgEnLf5r0DGbKaopvYwP-KMUJiiWspUVU6--JvPo3eATXhTWXSLhdRzSzite8dYNBXHfwWwSjMoiIrWCvWMQxNwcxfwPwQihoRNvXM5_-a_i_-N5ZwLk0hD359-Wa9cEJCdRMdwc=w733-h977-s-no?authuser=0" alt="Image of the 3 bands wrapped around the user leg" width="400"/>

