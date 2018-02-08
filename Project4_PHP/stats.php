<?php
# stats.php
#
# Author: Noah Williamson
# Last edit: 11/20/2017 
# CS316 Project 4 
#
# parses JSON data about sports and lets the user search for statistics
# which are in another JSON file

$filename_finder = array(); # used to find filename without showing user

# draws appropriate html form based on data in Sports.json
function drawForm(){
  $sport_contents = file_get_contents('Sports.json');
  $sport_results = json_decode($sport_contents); # we need this for our form

  # start writing html
  echo '
  <html>
    <head>
      <title>FanXelk</title>
      <style>
        form{ display:table;}
        p{ display:table-row; }
        label{ display:table-cell; }
        input{ display:table-cell; }
      </style>
    </head>
    <body>
      <h1>
          UK Sports Statistics:
      </h1>

      <form action="williamson_p4.php" method="get">
        <p><label for="title">Sport:</label>';

  $titles = array();
  $result = array();
  $searchterms = array(); # arrays from json data to help make form
  foreach($sport_results->sport as $elem){
    foreach($elem as $key => $value){
      if($key === "title")
        $titles[] = $value;
      if($key === "results")
        $result[] = $value;
      if($key === "searchterms")
        $searchterms[] = $value;
    }
  }

  # make hash for finding the filename later on
  global $filename_finder;
  for($i = 0; $i < count($titles); $i++){
    $key = $titles[$i];
    $filename_finder[$key] = $result[$i];
  }

  echo '<select id="title" name="title" style="width: 200px">';

  # start making form dynamically
  foreach($titles as $elem)
    echo "<option value=\"$elem\"> $elem </option>\n";

  echo '</p></select><p><label for="results">Results:</label>';
  echo '<select id="results" name="results" style="width: 200px">';

  foreach($result as $elem)
    foreach($elem as $key => $value)
      echo "<option value=\"$key\"> $key </option>\n";

  echo '</select></p>';
  echo '<p><label for="searchterm">Search terms: &emsp;</label>';
  echo '<select id="searchterm" name="searchterm" style="width: 200px">';
  echo '<option value=""> None </option>';

  $added = array(); # used to avoid duplicate search terms
  foreach($searchterms as $elem)
    foreach($elem as $term){
      if(!in_array($term, $added))
        echo "<option value=\"$term\"> $term </option>\n";

      $added[] = $term;
    }
  echo '</select></p>
        <br><input type="submit" value="Search">
      </form>';

}

# print the results given JSON filename with search term in bold 
function showResults($filename, $searchterm){
	if(file_exists($filename)){
		$contents = file_get_contents($filename);
		$results = json_decode($contents);

		# check if error in decode and give error msg
		if(json_last_error() !== JSON_ERROR_NONE){
			echo "<p style=\"font-weight:bold; color:red;\">";
      echo "ERROR: <br> Error with JSON data <br></p>";
			return;
		}
		
		$winCount = 0;
		$totalGames = 0; # counters
		
		# create header	
		echo "<h4>";
		foreach($results->comments as $elem){
			echo "$elem<br>";	
		}
    echo '</h4>';    

		# iterate through each element in games
		foreach($results->games as $element){
			
			# then iterate through each key value pair
			foreach($element as $key => $value){
        $newValue = str_replace("_", " ", $value); # clean up team names

        if($key === $searchterm){ # check if search term, then bold if so
          echo "<p style=\"font-weight:bold; color:blue;\">";
          echo "$key : $newValue </p>";
        }
        else{   # otherwise print normally
          echo "<p> $key : $newValue </p>"; 
        }

				# check if win and update count if necessary
				if($key === "WinorLose" && $value === "W")
					++$winCount;
			}
			++$totalGames;	# increment game count regardless
		  echo "<br>";
      
    }

		$winPercentage = ($winCount / $totalGames) * 100;
		echo "<br><p style=\"color:blue;\">";
    echo "Win percentage: $winPercentage % </p><br></body></html>";		
	
	}
	else{		# give error if file not found
		echo "<p style=\"font-weight:bold; color:red;\">";
    echo "No results found for the specified input.</p></body></html>";
		
    return;
	}
}

drawForm();   # draw html form no matter what

# check if our get parameters are set
if( isset( $_GET['title'] ) && isset( $_GET['results'] ) &&
                        isset( $_GET['searchterm'] ) ){
  $title_input = $_GET['title'];
  $results_input = $_GET['results'];
  $search_input = $_GET['searchterm']; # get params
  
  # find the filename
  $files = array();
  $filename = "";

  if( array_key_exists($title_input, $filename_finder) ){
    $files = $filename_finder[$title_input];
    foreach($files as $key => $val){
      if($key === $results_input)
        $filename = $val;
    }
  }

  # now print results
  showResults($filename, $search_input);
}

?>

