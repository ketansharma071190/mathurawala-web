# Always-on content drop creatives (pre-festival). Reuses photo_poster from the festival generator.
import build_festival_creatives as B
A=B.A; GOLD2=B.GOLD2; GOLDL=B.GOLDL
jobs=[
 ("post-ao-bedai.jpg","new-bedai-sabji.jpg","Mathura ka asli nashta","Subah, Mathura wali","Kachori-Bedai.",
  "Crisp, dal-bhari, haath se bani, taaza tali hui. Jaise Mathura mein hoti hai, waise hi.",104),
 ("post-ao-lassi.jpg","new-kulhad-lassi.jpg","Kulhad ki thandak","Garmi ka jawab,","Mathura wali Lassi.",
  "Malai se bhari, kesar aur pista ke saath, mitti ke kulhad mein. Ek ghoont aur Mathura yaad aa jaaye.",96),
 ("post-ao-rabdi.jpg","new-kesar-rabdi.jpg","Dheere, ghanton pakaai gayi","","Kesar Rabdi.",
  "Doodh ko ghanton kam kiya, kesar aur mewa dala, thandi parosi. Mathura ki asli mithaas.",150),
 ("post-ao-jalebi.jpg","latest-jalebi.jpg","Kadhai se seedhi plate mein","Garam, taaza","Jalebi.",
  "Ghee mein abhi bani, crisp aur ras se bhari. Subah ki shuruaat Mathura ke andaaz mein.",150),
]
for name,photo,kick,ls,lb,cap,bf in jobs:
    B.photo_poster(name, A(photo), kick, GOLDL, ls, lb, GOLD2, cap, big_font=bf)
print("alwayson done")
