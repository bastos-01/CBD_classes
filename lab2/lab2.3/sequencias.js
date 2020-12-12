sequencias = function () {

	var  numbers = db.phones.find({},{"display":  1}).toArray(); //store all numbers
	var  numbers_with_seq = [] //array to save arrays of sequences

    for(var j=1; j<numbers.length; j++){
        var  lista = [] //array to save each sequence
        previous_num = numbers[j-1].display.split("-")[1] //previous number
        current_num =  numbers[j].display.split("-")[1] //current number

        while(previous_num == current_num - 1){ //while previous equals current, is a sequence
            //include sequence numbers and avoiding repeted numbers
            if(!lista.includes(previous_num)) 
                lista.push(previous_num)
            if(!lista.includes(current_num))
                lista.push(current_num)
            j++
            //updating previous and current numbers to next iteration
            previous_num = numbers[j-1].display.split("-")[1]
            current_num =  numbers[j].display.split("-")[1]
        }

        //in case of sequence add to array
        if(lista.length > 0)
            numbers_with_seq.push(lista)

    }

	return  numbers_with_seq
}