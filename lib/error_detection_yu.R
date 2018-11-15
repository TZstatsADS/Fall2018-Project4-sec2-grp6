library(stringr)

rule1 <- function(string){
  # If a string is more than 20 characters in length, it is garbage. 
  # Example: iiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiii...
  if (nchar(string) > 20){
    return(TRUE)
  }else{
    return(FALSE)
  }
}

rule2 <- function(string){
  # If the number of punctuation characters in a string is greater 
  # than the number of alphanumeric characters, it is garbage.
  # Example: string = '?3//la‘'
  
  library(stringr)
  punc <- str_locate_all(string, "[:punct:]")
  punc_num <- dim(punc[[1]])[1]
  alnum <- str_locate_all(string, "[:alnum:]")
  alnum_num <- dim(alnum[[1]])[1]
  
  if ( punc_num > alnum_num){
    return(TRUE)
  }else{
    return(FALSE)
  }

}

rule3 <- function(string){
  # Ignoring the first and last characters in a string, 
  # if there are two or more different punctuation characters in the string, it is garbage.
  # Example: string = 'b?bl@bjk.1e.322'
  sub <- substr(string, 2, nchar(string)-1)
  punc <- str_locate_all(sub, "[:punct:]")
  punc_num <- dim(punc[[1]])[1]
  
  if ( punc_num >= 2){
    return(TRUE)
  }else{
    return(FALSE)
  }
  
}

rule4 <- function(string){
  # If there are three or more identical characters in a row in a string, it is garbage.
  # Example: string = 'aaaaaBlE'
  if (any(table(strsplit(string, '')[[1]]) >=3)){
    return(TRUE)
  }else{
    return(FALSE)
  }
  
}

rule5 <- function(string){
  # If the number of uppercase characters in a string is greater than 
  # the number of lowercase characters, 
  # and if the number of uppercase characters is less than 
  # the total number of characters in the string, it is garbage.
  # Example: string = 'BBEYaYYq'

  upper <- str_locate_all(string, "[[:upper:]]")
  upper_num <- dim(upper[[1]])[1]
  
  lower <- str_locate_all(string, "[[:lower:]]")
  lower_num <- dim(lower[[1]])[1]
  
  if ( (upper_num > lower_num) & (upper_num < nchar(string)) ){
    return(TRUE)
  }else{
    return(FALSE)
  }
}


rule6 <- function(string){
  # If all the characters in a string are alphabetic, 
  # and if the number of consonants in the string is greater than 8
  # times the number of vowels in the string, or vice-versa, it is garbage.
  # Example: string =  'jabwqbpP'
  alpha <- str_locate_all(string, "[[:alpha:]]")
  alpha_num <- dim(upper[[1]])[1]
  
  nvowels = str_count(tolower(string), "[aeoiu]")
  ncons = str_count(tolower(string), "[^aeoiu]")
  
  if(alpha_num == nchar(string)){
    if((ncons > (8*nvowels)) | (nvowels > (8*ncons))){
      return(TRUE)
    }
  }else{
    return(FALSE)
  }
  
}



rule7 <- function(string){
  # If there are four or more consecutive vowels in the string 
  # or five or more consecutive consonants in the string, it is garbage.
  # Example: string = 'buauub'
  cond1 <- grepl("[aeoiu]{1}[aeoiu]{1}[aeoiu]{1}[aeoiu]{+}",tolower(string))
  cond2 <- grepl("[bcdfghjklmnpqrstuvwxyz]{1}[bcdfghjklmnpqrstuvwxyz]{1}[bcdfghjklmnpqrstuvwxyz]{+}",tolower(string))
  if (cond1 | cond2){
    return(TRUE)
  }else{
    return(FALSE)
  }
}



rule8 <- function(string){
  # If the first and last characters in a string are both lowercase 
  # and any other character is uppercase, it is garbage.
  # Example: string = 'awwgrapHic'
  first <- substr(string, 1,1)
  sub <- substr(string, 2, nchar(string)-1)
  last <- substr(string, nchar(string),nchar(string))
  
  if(grepl("[[:lower:]]",first) & grepl("[[:lower:]]",last) & grepl("[[:upper:]]",sub)) {
    return(TRUE)
  }else{
    return(FALSE)
  }
}

error_detection <- function(string){
  if((rule1(string)) | (rule2(string)) |(rule3(string)) |(rule4(string)) |
     (rule5(string)) |(rule6(string)) |(rule7(string)) |(rule8(string)) ){
    return(TRUE)
  }else{
    return(FALSE)
  }
  
}

