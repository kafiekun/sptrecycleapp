<html>
 <body>
  <head>
   <title>
     run
   </title>
  </head>

   <form method="post">

    <input type="submit" value="GO" name="GO">
   </form>
 </body>
</html>

<?php
	if(isset($_POST['GO']))
	{
        $pythonScript = escapeshellcmd("python main.py");
		$output = shell_exec($pythonScript);
        echo $output;
	}
?>