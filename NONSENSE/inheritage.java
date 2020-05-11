public class inheritage {
	public class superclass{
		private String department;
		private String speciality;
		public superclass(String department,String speciality){
			this.setDepartment(department);
			this.setSpeciality(speciality);
		}
		public String getDepartment(){
			return this.department;
			}
		public void setDepartment(String department){
			this.department=department;
			}
		public String getSpeciality(){
			return this.speciality;
			}
		public void setSpeciality(String speciality){
			this.speciality=speciality;
			}
		}
	public class extendedclass extends superclass{
		private String subject;
		private String course;
		public extendedclass(String department,String speciality,String subject,String course){
			super(department,speciality);
			this.setSubject(subject);
			this.setCourse(course);
			}
		public String getSubject(){
			return this.subject;
			}
		public void setSubject(String subject){
			this.subject=subject;
			}
		public String getCourse(){
			return this.course;
			}
		public void setCourse(String course){
			this.course=course;
			}
		}
	public static void main(String[]args){
		}
	}
